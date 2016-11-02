import FWCore.ParameterSet.Config as cms
from Configuration.Generator.Pythia8CommonSettings_cfi import *
from Configuration.Generator.Pythia8CUEP8M1Settings_cfi import *
from GeneratorInterface.EvtGenInterface.EvtGenSetting_cff import *

generator = cms.EDFilter("Pythia8GeneratorFilter",
                         pythiaPylistVerbosity = cms.untracked.int32(0),
                         pythiaHepMCVerbosity = cms.untracked.bool(False),
                         comEnergy = cms.double(13000.0),
                         ##crossSection = cms.untracked.double(54000000000), # Given by PYTHIA after running
                         ##filterEfficiency = cms.untracked.double(0.004), # Given by PYTHIA after running
                         maxEventsToPrint = cms.untracked.int32(0),


                         ExternalDecays = cms.PSet(
        EvtGen130 = cms.untracked.PSet(
            decay_table = cms.string('GeneratorInterface/EvtGenInterface/data/DECAY_2010.DEC'),
            particle_property_file = cms.FileInPath('GeneratorInterface/EvtGenInterface/data/evt.pdl'),
            user_decay_file = cms.vstring('GeneratorInterface/ExternalDecays/data/LambdaB_Lambdamumu_ppi.dec'),
            list_forced_decays = cms.vstring('MyLambda_b0','Myanti-Lambda_b0'),
            operates_on_particles = cms.vint32()
            ),
        parameterSets = cms.vstring('EvtGen130')
        ),


                         PythiaParameters = cms.PSet(pythia8CommonSettingsBlock,
                                                     pythia8CUEP8M1SettingsBlock,
                                                     ## check this (need extra parameters?)
                                                     processParameters = cms.vstring("SoftQCD:nonDiffractive = on"),
                                                     parameterSets = cms.vstring('pythia8CommonSettings',
                                                                                 'pythia8CUEP8M1Settings',
                                                                                 'processParameters',
                                                                                 )
                                                     )
                         )

generator.PythiaParameters.processParameters.extend(EvtGenExtraParticles)

configurationMetadata = cms.untracked.PSet(
    version = cms.untracked.string('$Revision: 1.1 $'),
    name = cms.untracked.string('$Source: Configuration/Generator/python/PYTHIA8_LambdaB2LambdaMuMu_EtaPtFilter_CUEP8M1_13TeV_cff.py $'),
    annotation = cms.untracked.string('Summer16: Pythia8+EvtGen130 generation of LambdaB --> mu+ mu- Lambda (-> p pi) , 13TeV, Tune CUETP8M1')
    )

###########
# Filters #
###########

bfilter = cms.EDFilter(
    "PythiaFilter", 
    MaxEta = cms.untracked.double(9999.),
    MinEta = cms.untracked.double(-9999.),
    ParticleID = cms.untracked.int32(5122)  ## LambdaB
    )

decayfilter = cms.EDFilter(
    "PythiaDauVFilter",
    verbose         = cms.untracked.int32(1),
    NumberDaughters = cms.untracked.int32(3),
    ParticleID      = cms.untracked.int32(5122),
    DaughterIDs     = cms.untracked.vint32(-13, 13, 3122),  ## mu+, mu-, Lambda0
    MinPt           = cms.untracked.vdouble(2.5, 2.5, -1.),
    MinEta          = cms.untracked.vdouble(-2.5, -2.5, -9999.),
    MaxEta          = cms.untracked.vdouble( 2.5,  2.5,  9999.)
    )

lambdafilter = cms.EDFilter(
    "PythiaDauVFilter",
    verbose         = cms.untracked.int32(1), 
    NumberDaughters = cms.untracked.int32(2), 
    MotherID        = cms.untracked.int32(5122),  ## LambdaB
    ParticleID      = cms.untracked.int32(3122),  ## Lambda0
    DaughterIDs     = cms.untracked.vint32(2212, -211), ## p, pi-
    MinPt           = cms.untracked.vdouble(0.4, 0.4), 
    MinEta          = cms.untracked.vdouble(-2.5, -2.5), 
    MaxEta          = cms.untracked.vdouble( 2.5,  2.5)
    )


ProductionFilterSequence = cms.Sequence(generator*bfilter*decayfilter*lambdafilter)
