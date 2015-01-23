import FWCore.ParameterSet.Config as cms

## ------------------------------------------------------------------------
## MVA MET following POG recommendations
##  - https://twiki.cern.ch/twiki/bin/viewauth/CMS/MVAMet#CMSSW_7_2_X_requires_slc6
##  - https://github.com/cms-met/cmssw/blob/72X-mvaMETForMiniAOD/RecoMET/METPUSubtraction/test/testMVAMetProducer.py
##  - MVA MET needs the calibrated jets and the selected leptons as close
##    in the selection as used for the final analysis. It is in the user's
##    responsibility to define those and to pass them on to the mvaMet
##    producer.

## conditions needed for the JEC applied inside the MVA MET
from Configuration.StandardSequences.FrontierConditions_GlobalTag_cff import *
from JetMETCorrections.Configuration.JetCorrectionProducers_cff import *

## ------------------------------------------------------------------------
## calibrated jets and Type1 MET corrections as input for mvaMET producer
##  - NOTE: use "ak5PFL1FastL2L3" for MC / "ak5PFL1FastL2L3Residual" for
##    data

##  - NOTE: apparently "ak5PFL1FastL2L3" does not work
mvaMETJets = cms.EDProducer('PFJetCorrectionProducer',
    src = cms.InputTag('ak4PFJets'),
    correctors = cms.vstring("ak4PFL1FastL2L3")
    )

from RecoJets.JetProducers.pileupjetidproducer_cfi import pileupJetIdEvaluator
from RecoJets.JetProducers.PileupJetIDParams_cfi import JetIdParams
puJetIdForPFMVAMEt = pileupJetIdEvaluator.clone(
    algos = cms.VPSet(
    cms.PSet(
    tmvaVariables = cms.vstring(
        "nvtx",
        "jetPt",
        "jetEta",
        "jetPhi",
        "dZ",
        "beta",
        "betaStar",
        "nCharged",
        "nNeutrals",
        "dR2Mean",
        "ptD",
        "frac01",
        "frac02",
        "frac03",
        "frac04",
        "frac05"
    ),
    tmvaWeights = cms.string("RecoJets/JetProducers/data/TMVAClassificationCategory_JetID_MET_53X_Dec2012.weights.xml"),
    tmvaMethod = cms.string("JetID"),
    tmvaSpectators = cms.vstring(),
    JetIdParams = JetIdParams,
    impactParTkThreshold = cms.double(0.),
    version = cms.int32(-1),
    cutBased = cms.bool(False),
    label = cms.string("full")
    )
    ),
    produceJetIds = cms.bool(True),
    runMvas = cms.bool(True),
    jets = cms.InputTag("mvaMETJets"),
    applyJec = cms.bool(True),
    inputIsCorrected = cms.bool(True),
    jec = cms.string("AK4PF"),
    )

# the following two statements have been widely restricted and deactivated since they caused Kappa to crash
from JetMETCorrections.Type1MET.correctionTermsPfMetType1Type2_cff import corrPfMetType1
#from JetMETCorrections.Type1MET.correctedMet_cff import *

corrPfMetType1.jetCorrLabel = "ak4PFL1FastL2L3" 

## ------------------------------------------------------------------------
## muons as input for mvaMET producer
mvaMETMuons = cms.EDFilter("MuonSelector",
    src = cms.InputTag('muons'),
    cut = cms.string(
        "abs(eta)<2.1 & pt>15"                                      +
        ## muon ID
        "& isTrackerMuon"                                           +
        "& isPFMuon"                                                +
        "& globalTrack.isNonnull"                                   +
        "& innerTrack.hitPattern.numberOfValidPixelHits    >  0"    +
        "& innerTrack.normalizedChi2                       < 10"    +
        "& numberOfMatches                                 >  0"    +
        "& innerTrack.hitPattern.numberOfValidTrackerHits  >  5"    +
        "& globalTrack.hitPattern.numberOfValidHits        >  0"    +
        "& abs(innerTrack().dxy)                           <2.0"    +
        ## muon isolation (w/o deltaBeta, therefore weaker selection criteria)
        "& (pfIsolationR03.sumChargedHadronPt+pfIsolationR03.sumNeutralHadronEt+pfIsolationR03.sumPhotonEt)/pt < 0.3"
    ),
    filter = cms.bool(False)
    )

## ------------------------------------------------------------------------
## electrons as input for mvaMET producer
mvaMETElectrons = cms.EDFilter("GsfElectronSelector",
    src = cms.InputTag('gedGsfElectrons'),
    cut = cms.string(
        "abs(eta) < 2.3 && pt > 15"                                          +
        "&& gsfTrack.hitPattern().numberOfHits(\'MISSING_INNER_HITS\') == 0" + 
        ## electron ID for barrel electrons
        "&& ((abs(eta) < 1.4442  "                                           +
        "&& abs(deltaEtaSuperClusterTrackAtVtx)            < 0.007"          +
        "&& abs(deltaPhiSuperClusterTrackAtVtx)            < 0.8"            +
        "&& sigmaIetaIeta                                  < 0.01"           +
        "&& hcalOverEcal                                   < 0.15"           +
        "&& abs(1./superCluster.energy - 1./p)             < 0.05)"          +
        ## electron ID for endcap electrons
        "|| (abs(eta)  > 1.566 "                                             +
        "&& abs(deltaEtaSuperClusterTrackAtVtx)            < 0.009 "         +
        "&& abs(deltaPhiSuperClusterTrackAtVtx)            < 0.10"           +
        "&& sigmaIetaIeta                                  < 0.03"           +
        "&& hcalOverEcal                                   < 0.10"           +
        "&& abs(1./superCluster.energy - 1./p)             < 0.05))"         +
        ## electron isolation (w/o deltaBeta, therefore weaker selection criteria)
        "&& (pfIsolationVariables.sumChargedHadronPt+pfIsolationVariables.sumNeutralHadronEt)/et < 0.3"
        ),
    filter = cms.bool(False)
    )                                                

## ------------------------------------------------------------------------
## taus as input for mvaMET producer
##  - NOTE that the selection for taus depends on the final state
mvaMETTausET = cms.EDFilter("PFTauSelector",
    src = cms.InputTag('hpsPFTauProducer'),
    BooleanOperator = cms.string("and"),
    discriminators = cms.VPSet(              
        cms.PSet( discriminator=cms.InputTag("hpsPFTauDiscriminationByDecayModeFinding"                       ), selectionCut=cms.double(0.5)),
        cms.PSet( discriminator=cms.InputTag("hpsPFTauDiscriminationByLooseCombinedIsolationDBSumPtCorr3Hits" ), selectionCut=cms.double(0.5)),
        cms.PSet( discriminator=cms.InputTag("hpsPFTauDiscriminationByLooseElectronRejection"                 ), selectionCut=cms.double(0.5)),
        cms.PSet( discriminator=cms.InputTag("hpsPFTauDiscriminationByLooseMuonRejection"                     ), selectionCut=cms.double(0.5)) 
        ),
    cut = cms.string("abs(eta) < 2.3 && pt > 20.0 "),
    filter = cms.bool(False)
    )

mvaMETTausMT = cms.EDFilter("PFTauSelector",
    src = cms.InputTag('hpsPFTauProducer'),
    BooleanOperator = cms.string("and"),
    discriminators = cms.VPSet(              
        cms.PSet( discriminator=cms.InputTag("hpsPFTauDiscriminationByDecayModeFinding"                       ), selectionCut=cms.double(0.5)),
        cms.PSet( discriminator=cms.InputTag("hpsPFTauDiscriminationByLooseCombinedIsolationDBSumPtCorr3Hits" ), selectionCut=cms.double(0.5)),
        cms.PSet( discriminator=cms.InputTag("hpsPFTauDiscriminationByLooseElectronRejection"                 ), selectionCut=cms.double(0.5)),
        cms.PSet( discriminator=cms.InputTag("hpsPFTauDiscriminationByTightMuonRejection"                     ), selectionCut=cms.double(0.5)) 
        ),
    cut = cms.string("abs(eta) < 2.3 && pt > 20.0 "),
    filter = cms.bool(False)
    )

mvaMETTausTT = cms.EDFilter("PFTauSelector",
    src = cms.InputTag('hpsPFTauProducer'),
    BooleanOperator = cms.string("and"),
    discriminators = cms.VPSet(              
        cms.PSet( discriminator=cms.InputTag("hpsPFTauDiscriminationByDecayModeFinding"                       ), selectionCut=cms.double(0.5)),
        cms.PSet( discriminator=cms.InputTag("hpsPFTauDiscriminationByMediumCombinedIsolationDBSumPtCorr3Hits"), selectionCut=cms.double(0.5)),
        cms.PSet( discriminator=cms.InputTag("hpsPFTauDiscriminationByLooseElectronRejection"                 ), selectionCut=cms.double(0.5)),
        cms.PSet( discriminator=cms.InputTag("hpsPFTauDiscriminationByLooseMuonRejection"                     ), selectionCut=cms.double(0.5)) 
        ),
    cut = cms.string("abs(eta) < 2.3 && pt > 20.0 "),
    filter = cms.bool(False)
    )

## ------------------------------------------------------------------------
## MVA MET
##  - srcLeptons nees a collectino of lepton as close as possible to the
##    leptons selected for the analysis.
##  - srcCorrJets/srcUncorrJets should correspond to the jets as used in
##    the analysis. 
from RecoJets.JetProducers.PileupJetIDParams_cfi import JetIdParams

pfMetMVA = cms.EDProducer(
    "PFMETProducerMVA",
    srcCorrJets       = cms.InputTag('mvaMETJets'),
    srcUncorrJets     = cms.InputTag('ak5PFJets'),
    srcMVAPileupJetId = cms.InputTag('puJetIdForPFMVAMEt','fullDiscriminant'),
    srcPFCandidates   = cms.InputTag('particleFlow'),
    srcVertices       = cms.InputTag('goodOfflinePrimaryVertices'),
    srcLeptons        = cms.VInputTag(),
    minNumLeptons     = cms.int32(0),
    srcRho            = cms.InputTag('kt6PFJets','rho'),
    globalThreshold   = cms.double(-1.),#pfMet.globalThreshold,
    minCorrJetPt      = cms.double(-1.),
    inputFileNames    = cms.PSet(
        U     = cms.FileInPath('RecoMET/METPUSubtraction/data/gbrmet_53_Sep2013_type1.root'    ),
        DPhi  = cms.FileInPath('RecoMET/METPUSubtraction/data/gbrmetphi_53_June2013_type1.root'),
        CovU1 = cms.FileInPath('RecoMET/METPUSubtraction/data/gbru1cov_53_Dec2012.root'        ),
        CovU2 = cms.FileInPath('RecoMET/METPUSubtraction/data/gbru2cov_53_Dec2012.root'        ),
    ),
    loadMVAfromDB   = cms.bool(False),
    corrector       = cms.string("ak4PFL1Fastjet"),
    useType1        = cms.bool(True),
    dZcut           = cms.double(0.1),
    verbosity       = cms.int32(0)
)

## specify the leptons similar to those used in the analysis (channel specific)
pfMetMVAEM = pfMetMVA.clone(srcLeptons = cms.VInputTag("mvaMETElectrons", "mvaMETMuons" ))
pfMetMVAET = pfMetMVA.clone(srcLeptons = cms.VInputTag("mvaMETElectrons", "mvaMETTausET"))
pfMetMVAMT = pfMetMVA.clone(srcLeptons = cms.VInputTag("mvaMETMuons"    , "mvaMETTausMT"))
pfMetMVATT = pfMetMVA.clone(srcLeptons = cms.VInputTag("mvaMETTausTT"))

## ------------------------------------------------------------------------
## Definition of sequences
makeKappaMET = cms.Sequence(
    mvaMETJets *
    puJetIdForPFMVAMEt *
    mvaMETMuons *
    mvaMETTausET *
    mvaMETTausMT *
    mvaMETTausTT *
    mvaMETElectrons *
    pfMetMVAEM * 
    pfMetMVAET *
    pfMetMVAMT *
    pfMetMVATT 
    )