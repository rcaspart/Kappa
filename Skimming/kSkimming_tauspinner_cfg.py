import os
import sys
import FWCore.ParameterSet.Config as cms
import Kappa.Skimming.datasetsHelper as datasetsHelper

def getBaseConfig(globaltag= 'START53_V15A::All', testfile=cms.untracked.vstring(""), maxevents=100, nickname = 'SM_VBFHToTauTau_M_90_powheg_pythia_8TeV', kappaTag = 'Kappa_1_0_0'):

	from Kappa.Producers.KSkimming_template_cfg import process
	process.source.fileNames      = testfile
	process.maxEvents.input	      = maxevents				## number of events to be processed (-1 = all in file)
	process.kappaTuple.outputFile = 'kappaTuple.root'			## name of output file
	process.kappaTuple.verbose    = cms.int32(0)				## verbosity level
	if not globaltag.lower() == 'auto' :
		process.GlobalTag.globaltag   = globaltag
		print "GT (overwritten):", process.GlobalTag.globaltag
	data = datasetsHelper.isData(nickname)
	centerOfMassEnergy = datasetsHelper.getCenterOfMassEnergy(nickname)

	## ------------------------------------------------------------------------
	# Configure Metadata describing the file
	process.kappaTuple.active										= cms.vstring('TreeMetadata')
	process.kappaTuple.TreeMetadata.parameters = cms.PSet(
		dataset						= cms.string(datasetsHelper.getDatasetName(nickname)),
		generator					= cms.string(datasetsHelper.getGenerator(nickname)),
		productionProcess			= cms.string(datasetsHelper.getProcess(nickname)),
		globalTag					= cms.string(globaltag),
		prodCampaignGlobalTag	= cms.string(datasetsHelper.getProductionCampaignGlobalTag(nickname, centerOfMassEnergy)),
		runPeriod					= cms.string(datasetsHelper.getRunPeriod(nickname)),
		kappaTag						= cms.string(kappaTag),
		isEmbedded					= cms.bool(datasetsHelper.getIsEmbedded(nickname)),
		jetMultiplicity			= cms.int32(datasetsHelper.getJetMultiplicity(nickname)),
		centerOfMassEnergy		= cms.int32(centerOfMassEnergy),
		puScenario					= cms.string(datasetsHelper.getPuScenario(nickname, centerOfMassEnergy)),
		isData						= cms.bool(data)
		)


	## ------------------------------------------------------------------------
	# General configuration

	process.kappaTuple.active += cms.vstring('VertexSummary')	## save VertexSummary,
	process.kappaTuple.active += cms.vstring('BeamSpot')		## save Beamspot,
	process.kappaTuple.active += cms.vstring('TriggerObjects')

	if data:
		process.kappaTuple.active+= cms.vstring('DataMetadata')		## produce Metadata for data,
	else:
		process.kappaTuple.active+= cms.vstring('GenMetadata')		## produce Metadata for MC,
		process.kappaTuple.active+= cms.vstring('GenParticles')		## save GenParticles,
		process.kappaTuple.active+= cms.vstring('GenTaus')				## save GenParticles,

	process.kappaTuple.Metadata.hltWhitelist = cms.vstring(			## HLT selection
		# https://github.com/cms-analysis/HiggsAnalysis-KITHiggsToTauTau/blob/master/data/triggerTables-2011-2012.txt
		# e
		"^HLT_Ele[0-9]+_CaloIdVT_(CaloIsoT)?_TrkIdT_(TrkIsoT)?_v[0-9]+$",
		"^HLT_Ele[0-9]+_WP[0-9]+_v[0-9]+$",
		# m
		"^HLT_(Iso)?Mu[0-9]+_(eta2p1)?_v[0-9]+$",
		# ee
		"^HLT_Ele[0-9]+_CaloId(L|T)(_TrkIdVL)?_CaloIsoVL(_TrkIdVL)?(_TrkIsoVL)?" +
			"_Ele[0-9]+_CaloId(L|T)(_TrkIdVL)?_CaloIsoVL(_TrkIdVL)?(_TrkIsoVL)?_v[0-9]+$",
		# mm
		"^HLT_(Double)Mu[0-9]+(_(Mu|Jet)[0-9]+)?_v[0-9]+$",
		# em
		"^HLT_Mu[0-9]+_(Ele|Photon)[0-9]+_CaloId(L|T|VT)(_CaloIsoVL|_IsoT)?(_TrkIdVL_TrkIsoVL)?_v[0-9]+$",
		# et
		"^HLT_Ele[0-9]+_CaloIdVT(_Calo(IsoRho|Iso)T)?_TrkIdT(_TrkIsoT)?_(Loose|Medium|Tight)IsoPFTau[0-9]+_v[0-9]+$",
		"^HLT_Ele[0-9]+_eta2p1_WP[0-9]+(Rho|NoIso)_LooseIsoPFTau[0-9]+_v[0-9]+$",
		# mt
		"^HLT_(Iso)?Mu[0-9]+(_eta2p1)?_(Loose|Medium|Tight)IsoPFTau[0-9]+(_Trk[0-9]_eta2p1)?_v[0-9]+$",
		# tt
		"^HLT_Double(Medium)?IsoPFTau[0-9]+_Trk1_eta2p1_(Jet[0-9]+|Prong[0-9])?_v[0-9]+$",
		"^HLT_Double(Medium)?IsoPFTau[0-9]+_Trk5_eta2p1_(Jet[0-9]+|Prong[0-9])?_v[0-9]+$",
		"^HLT_Double(Medium)?IsoPFTau[0-9]+_Trk1_eta2p1_v[0-9]+$",
		"^HLT_Double(Medium)?IsoPFTau[0-9]+_Trk5_eta2p1_v[0-9]+$",
		# specials (possible generalization: Mu15, L1ETM20, Photon20, Ele8)
		"^HLT_Ele[0-9]+_CaloId(L|T|VT)_CaloIso(VL|T|VT)(_TrkIdT)?(_TrkIsoVT)?_(SC|Ele)[0-9](_Mass[0-9]+)?_v[0-9]+$",
		"^HLT_Ele8_v[0-9]+$",
		"^HLT_IsoMu15(_eta2p1)?_L1ETM20_v[0-9]+$",
		"^HLT_Photon20_CaloIdVT_IsoT_Ele8_CaloIdL_CaloIsoVL_v[0-9]+$",
		)

	process.kappaTuple.Metadata.hltFailToleranceList = cms.vstring(
		"hltDoubleL2Tau35eta2p1",
		"hltL2Tau25eta2p1",
		"hltL2Tau25eta2p1",
		"hltL2fL1sMu16Eta2p1L1f0L2Filtered16Q",
		"hltDoubleL2Tau30eta2p1",
		"hltL2Tau25eta2p1"
		)

	# disable overrideHLTCheck for embedded samples, since it triggers an Kappa error
	process.kappaTuple.Metadata.overrideHLTCheck = cms.untracked.bool(datasetsHelper.getIsEmbedded(nickname))


	## ------------------------------------------------------------------------
	## TauSpinner
	process.load("Kappa.Producers.KTauSpinner_cff")
	process.kappaTuple.active += cms.vstring('TauSpinner')

	## ------------------------------------------------------------------------
	## MET
#	process.load("Kappa.Producers.KMET_cff")
#	process.kappaTuple.active += cms.vstring('MET')                         ## produce/save KappaMET
#	process.kappaTuple.active += cms.vstring('PFMET')                       ## produce/save KappaPFMET

	## ------------------------------------------------------------------------
	## And let it run
	process.p = cms.Path(
		process.TauSpinnerReco *
		process.kappaOut
		)

	## ------------------------------------------------------------------------
	## declare edm OutputModule (expects a path 'p'), uncommented if wanted

#	process.edmOut = cms.OutputModule(
#		"PoolOutputModule",
#		fileName = cms.untracked.string('dump.root'),				## name of output file
#		SelectEvents = cms.untracked.PSet( SelectEvents = cms.vstring('p') ),	## save only events passing the full path
#		outputCommands = cms.untracked.vstring('drop *', 'keep *_*_*_KAPPA')	## save each edm object that has been produced by process KAPPA
#		)
#	process.ep = cms.EndPath(process.edmOut)

	return process

if __name__ == "__main__":
	if('@' in '@NICK@'): # run local skim by hand without replacements by grid-control
		## test file for EKP
		#testfile	= cms.untracked.vstring('file:/storage/8/dhaitz/testfiles/mc11.root')
		#testfile	= cms.untracked.vstring('file:/storage/6/berger/testfiles/data_2012C_AOD.root')
		## test file for lxplus
		testfile	= cms.untracked.vstring('file:/storage/a/friese/aod/VBF-Htautau.root')
		## test file for RWTH
		#testfile	= cms.untracked.vstring('file:/user/kargoll/testfiles/DYTauTau/DYTauTau_Summer12.root')
		process = getBaseConfig(testfile = testfile)

	## for grid-control:
	else:
		process = getBaseConfig('@GLOBALTAG@', nickname = '@NICK@', kappaTag = '@KAPPA_TAG@')



