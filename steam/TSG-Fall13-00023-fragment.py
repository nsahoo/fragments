import FWCore.ParameterSet.Config as cms

generator = cms.EDFilter("Pythia8GeneratorFilter",
	comEnergy = cms.double(13000.0),
	crossSection = cms.untracked.double(1.643e9),
	filterEfficiency = cms.untracked.double(1),
	maxEventsToPrint = cms.untracked.int32(0),
	pythiaHepMCVerbosity = cms.untracked.bool(False),
	pythiaPylistVerbosity = cms.untracked.int32(0),

	PythiaParameters = cms.PSet(
		processParameters = cms.vstring(
			'Main:timesAllowErrors    = 10000',
			#'ParticleDecays:limitTau0 = on',
			#'ParticleDecays:tauMax = 10',
			'HardQCD:all = on',
			'PhaseSpace:pTHatMin = 30 ',
			'PhaseSpace:pTHatMax = 50 ',
			'Tune:pp 5',
			'Tune:ee 3',
            'ParticleDecays:limitCylinder = on',
	        'ParticleDecays:xyMax=2000',
	        'ParticleDecays:zMax=4000',
            '130:mayDecay = on',
            '211:mayDecay = on',
            '321:mayDecay = on'
		),
		parameterSets = cms.vstring('processParameters')
	)
)

mugenfilter = cms.EDFilter("MCSmartSingleParticleFilter",
                           MinPt = cms.untracked.vdouble(5.,5.),
                           MinEta = cms.untracked.vdouble(-2.5,-2.5),
                           MaxEta = cms.untracked.vdouble(2.5,2.5),
                           ParticleID = cms.untracked.vint32(13,-13),
                           Status = cms.untracked.vint32(1,1),
                           # Decay cuts are in mm
                           MaxDecayRadius = cms.untracked.vdouble(2000.,2000.),
                           MinDecayZ = cms.untracked.vdouble(-4000.,-4000.),
                           MaxDecayZ = cms.untracked.vdouble(4000.,4000.)
)

configurationMetadata = cms.untracked.PSet(
	version = cms.untracked.string('\$Revision: 1.1 $'),
	annotation = cms.untracked.string('Fall13 sample with PYTHIA8: QCD dijet production, pThat = 30 .. 50 GeV, with INCLUSIVE muon preselection (pt(mu) > 5), Tune4C')
)

ProductionFilterSequence = cms.Sequence(generator*mugenfilter)
