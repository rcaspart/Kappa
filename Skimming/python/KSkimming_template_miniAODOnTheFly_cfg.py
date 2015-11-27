#-# Copyright (c) 2014 - All Rights Reserved
#-#   Fabio Colombo <fabio.colombo@cern.ch>
#-#   Joram Berger <joram.berger@cern.ch>
#-#   Raphael Friese <Raphael.Friese@cern.ch>
#-#   Roger Wolf <roger.wolf@cern.ch>

import FWCore.ParameterSet.Config as cms

process = cms.Process("KAPPA")


## MessageLogger
process.load("FWCore.MessageLogger.MessageLogger_cfi")
process.MessageLogger.default = cms.untracked.PSet(
	ERROR = cms.untracked.PSet(limit = cms.untracked.int32(5))
	#suppressError = cms.untracked.vstring("electronIdMVAProducer")
)

process.MessageLogger.cerr.FwkReport.reportEvery = 50

## Options and Output Report
#process.options = cms.untracked.PSet( allowUnscheduled = cms.untracked.bool(False) )
process.options = cms.untracked.PSet( wantSummary = cms.untracked.bool(True) ,
	allowUnscheduled = cms.untracked.bool(False) )

## Source
process.source = cms.Source("PoolSource",
	fileNames = cms.untracked.vstring()
)
## Maximal number of Events
process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(100) )

## Geometry and Detector Conditions (needed for a few patTuple production steps)
import Kappa.Skimming.tools as tools
cmssw_version_number = tools.get_cmssw_version_number()
split_cmssw_version = cmssw_version_number.split("_") 

process.load('Configuration.StandardSequences.Services_cff')
process.load('SimGeneral.HepPDTESSource.pythiapdt_cfi')
process.load('FWCore.MessageService.MessageLogger_cfi')
process.load('Configuration.EventContent.EventContent_cff')
process.load('SimGeneral.MixingModule.mixNoPU_cfi')
process.load('Configuration.StandardSequences.GeometryRecoDB_cff')
process.load('Configuration.StandardSequences.MagneticField_38T_cff')
process.load('PhysicsTools.PatAlgos.slimming.metFilterPaths_cff')
process.load('Configuration.StandardSequences.EndOfProcess_cff')
process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_condDBv2_cff')

process.configurationMetadata = cms.untracked.PSet(
	annotation = cms.untracked.string('step1 nevts:100'),
	name = cms.untracked.string('Applications'),
	version = cms.untracked.string('$Revision: 1.19 $')
)

process.MINIAODSIMoutput = cms.OutputModule("PoolOutputModule",
	compressionAlgorithm = cms.untracked.string('LZMA'),
	compressionLevel = cms.untracked.int32(4),
	dataset = cms.untracked.PSet(
		dataTier = cms.untracked.string('MINIAODSIM'),
		filterName = cms.untracked.string('')
	),
	dropMetaData = cms.untracked.string('ALL'),
	eventAutoFlushCompressedSize = cms.untracked.int32(15728640),
	fastCloning = cms.untracked.bool(False),
	fileName = cms.untracked.string('file:HIG-RunIISpring15MiniAODv2-00050.root'),
	outputCommands = process.MINIAODSIMEventContent.outputCommands,
	overrideInputFileSplitLevels = cms.untracked.bool(True)
)

process.Flag_trkPOG_toomanystripclus53X = cms.Path(~process.toomanystripclus53X)
process.Flag_EcalDeadCellBoundaryEnergyFilter = cms.Path(process.EcalDeadCellBoundaryEnergyFilter)
process.Flag_HBHENoiseIsoFilter = cms.Path(process.HBHENoiseFilterResultProducer+process.HBHENoiseIsoFilter)
process.Flag_trackingFailureFilter = cms.Path(process.goodVertices+process.trackingFailureFilter)
process.Flag_goodVertices = cms.Path(process.primaryVertexFilter)
process.Flag_hcalLaserEventFilter = cms.Path(process.hcalLaserEventFilter)
process.Flag_CSCTightHaloFilter = cms.Path(process.CSCTightHaloFilter)
process.Flag_trkPOGFilters = cms.Path(process.trkPOGFilters)
process.Flag_eeBadScFilter = cms.Path(process.eeBadScFilter)
process.Flag_trkPOG_manystripclus53X = cms.Path(~process.manystripclus53X)
process.Flag_METFilters = cms.Path(process.metFilters)
process.Flag_trkPOG_logErrorTooManyClusters = cms.Path(~process.logErrorTooManyClusters)
process.Flag_HBHENoiseFilter = cms.Path(process.HBHENoiseFilterResultProducer+process.HBHENoiseFilter)
process.Flag_EcalDeadCellTriggerPrimitiveFilter = cms.Path(process.EcalDeadCellTriggerPrimitiveFilter)
process.Flag_ecalLaserCorrFilter = cms.Path(process.ecalLaserCorrFilter)
process.endjob_step = cms.EndPath(process.endOfProcess)
process.MINIAODSIMoutput_step = cms.EndPath(process.MINIAODSIMoutput)

## Kappa
process.load('Kappa.Producers.KTuple_cff')
process.kappaTuple = cms.EDAnalyzer('KTuple',
    process.kappaTupleDefaultsBlock,
    outputFile = cms.string("kappaTuple.root"),
)
process.kappaTuple.active = cms.vstring()
process.kappaOut = cms.Sequence(process.kappaTuple)

process.p = cms.Path ()
process.ep = cms.EndPath()
process.load("Kappa.CMSSW.EventWeightCountProducer_cff")

