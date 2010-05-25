import FWCore.ParameterSet.Config as cms

# Basic process setup ----------------------------------------------------------
process = cms.Process("kappaSkim")
process.source = cms.Source("PoolSource", fileNames = cms.untracked.vstring(
	'file:///home/piparo/testFiles/Spring10_MinBias_GENSIMRECO_MC_3XY_V25_S09_preproduction-v2.root',
))
process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(1000) )
#-------------------------------------------------------------------------------

# Includes + Global Tag --------------------------------------------------------
process.load("FWCore.MessageService.MessageLogger_cfi")
process.load('Configuration/StandardSequences/Services_cff')
process.load('Configuration.StandardSequences.MagneticField_38T_cff')
process.load('RecoJets.Configuration.RecoJetAssociations_cff')
process.load('Configuration/StandardSequences/FrontierConditions_GlobalTag_cff')
process.GlobalTag.globaltag = '@GLOBALTAG@'
#-------------------------------------------------------------------------------

# Configure tuple generation ---------------------------------------------------
process.load("Kappa.Producers.KTuple_cff")
process.kappatuple = cms.EDAnalyzer('KTuple',
	process.kappaTupleDefaultsBlock,
	outputFile = cms.string('skim.root'),
	CaloJets = cms.PSet(
		srcNoiseHCAL = cms.InputTag("hcalnoise"),
		maxN = cms.int32(-1),
		minPt = cms.double(-1),
		maxEta = cms.double(-1),
		AK5CaloJets = cms.PSet(
			src = cms.InputTag("ak5CaloJets"),
			srcExtender = cms.InputTag("ak5JetExtender"),
			srcJetID = cms.InputTag("ak5JetID"),
		),
		AK7CaloJets = cms.PSet(
			src = cms.InputTag("ak7CaloJets"),
			srcExtender = cms.InputTag("ak7JetExtender"),
			srcJetID = cms.InputTag("ak7JetID"),
		),
		IC5CaloJets = cms.PSet(
			src = cms.InputTag("iterativeCone5CaloJets"),
			srcExtender = cms.InputTag("iterativeCone5JetExtender"),
			srcJetID = cms.InputTag("ic5JetID"),
		),
		SC5CaloJets = cms.PSet(
			src = cms.InputTag("sisCone5CaloJets"),
			srcExtender = cms.InputTag("sisCone5JetExtender"),
			srcJetID = cms.InputTag("sc5JetID"),
		),
		SC7CaloJets = cms.PSet(
			src = cms.InputTag("sisCone7CaloJets"),
			srcExtender = cms.InputTag(""),
			srcJetID = cms.InputTag("sc7JetID"),
		),
		KT4CaloJets = cms.PSet(
			src = cms.InputTag("kt4CaloJets"),
			srcExtender = cms.InputTag("kt4JetExtender"),
			srcJetID = cms.InputTag("kt4JetID")
		),
		KT6CaloJets = cms.PSet(
			src = cms.InputTag("kt6CaloJets"),
			srcExtender = cms.InputTag(""),
			srcJetID = cms.InputTag("kt6JetID")
		),
	)
)
process.kappatuple.verbose = cms.int32(0)
process.kappatuple.hltSource = cms.InputTag("TriggerResults::REDIGI")
process.kappatuple.active = cms.vstring(
	'Muons', 'Partons', 'TrackSummary', 'LV', 'MET', 'PFMET', 'CaloJets', 'PFJets', 'Vertex', 'GenMetadata', @ACTIVE@
)
#-------------------------------------------------------------------------------

# Process schedule -------------------------------------------------------------
process.pathDAT = cms.Path(process.recoJetAssociations+process.kappatuple)
process.schedule = cms.Schedule(process.pathDAT)
#-------------------------------------------------------------------------------
