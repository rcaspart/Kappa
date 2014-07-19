import FWCore.ParameterSet.Config as cms

RandomNumberGeneratorService = cms.Service("RandomNumberGeneratorService",
	TauSpinnerReco = cms.PSet(
		initialSeed = cms.untracked.uint32(2342452345),
		engineName = cms.untracked.string('TRandom3')
		)
	)


TauSpinnerReco = cms.EDProducer("TauSpinnerCMS",
	                            isReco = cms.bool(True),
	                            isTauolaConfigured = cms.bool(False),
	                            isLHPDFConfigured = cms.bool(False),
	                            LHAPDFname = cms.untracked.string('MSTW2008nnlo90cl.LHgrid'),
	                            CMSEnergy = cms.double(8000.0),
	                            gensrc = cms.InputTag('genParticles'),
	                            Ipol = cms.untracked.int32(1)
	                            )

makeKappaTauSpinner = cms.Sequence(
	TauSpinnerReco
	)
