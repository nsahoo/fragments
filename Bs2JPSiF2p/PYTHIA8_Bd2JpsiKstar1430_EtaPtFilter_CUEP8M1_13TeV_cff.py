import FWCore.ParameterSet.Config as cms

from Configuration.Generator.Pythia8CommonSettings_cfi import *
####from Configuration.Generator.MCTunes2017.PythiaCP5Settings_cfi import *
from Configuration.Generator.Pythia8CUEP8M1Settings_cfi import *
from GeneratorInterface.EvtGenInterface.EvtGenSetting_cff import *

generator = cms.EDFilter(
    "Pythia8GeneratorFilter",
    pythiaHepMCVerbosity = cms.untracked.bool(False),
    maxEventsToPrint = cms.untracked.int32(0),
    pythiaPylistVerbosity = cms.untracked.int32(0),
    filterEfficiency = cms.untracked.double(7.010e-01),
    crossSection = cms.untracked.double(540000000.),
    comEnergy = cms.double(13000.0),
    ExternalDecays = cms.PSet(
        EvtGen130 = cms.untracked.PSet(
            decay_table = cms.string('GeneratorInterface/EvtGenInterface/data/DECAY_2014_NOLONGLIFE.DEC'),
            particle_property_file = cms.FileInPath('GeneratorInterface/EvtGenInterface/data/evt_2014.pdl'),
            #user_decay_file = cms.vstring('GeneratorInterface/EvtGenInterface/data/Bd_JpsiKstar_mumuKpi.dec'),
            list_forced_decays = cms.vstring('MyB0', 'Myanti-B0'),
            operates_on_particles = cms.vint32(511),
            convertPythiaCodes = cms.untracked.bool(False),
            user_decay_embedded = cms.vstring(
"""
#
# This is the decay file for the decay B0 -> J/PSI K*(1430)
#
Alias      MyB0        B0
Alias      Myanti-B0   anti-B0
ChargeConj Myanti-B0   MyB0 
Alias      MyJpsi      J/psi
ChargeConj MyJpsi      MyJpsi
Alias      MyK*0       K_0*0
Alias      MyK*0bar    anti-K_0*0
ChargeConj MyK*0       MyK*0bar
#
Decay MyB0
  1.000    MyJpsi      MyK*0                   PHSP;
Enddecay
CDecay Myanti-B0
#
Decay MyJpsi
  1.000         mu+       mu-            PHOTOS VLL;
Enddecay
#
Decay MyK*0
  1.000        K+        pi-                   PHSP;
Enddecay
Decay MyK*0bar
  1.000        K-        pi+                   PHSP;
Enddecay 
End
"""
            ),
        ),
        parameterSets = cms.vstring('EvtGen130')
    ),
    PythiaParameters = cms.PSet(
        pythia8CommonSettingsBlock,
        ###pythia8CP5SettingsBlock,
        pythia8CUEP8M1SettingsBlock,
        processParameters = cms.vstring(
            "SoftQCD:nonDiffractive = on",
            'PTFilter:filter = on', # this turn on the filter
            'PTFilter:quarkToFilter = 5', # PDG id of q quark
            'PTFilter:scaleToFilter = 1.0'),
        parameterSets = cms.vstring(
            'pythia8CommonSettings',
            ###'pythia8CP5Settings',
            'pythia8CUEP8M1Settings',
            'processParameters',
        )
    )
)

bfilter = cms.EDFilter(
    "PythiaFilter",
    MaxEta = cms.untracked.double(9999.),
    MinEta = cms.untracked.double(-9999.),
    ParticleID = cms.untracked.int32(511)
)

jpsifilter = cms.EDFilter(
    "PythiaDauVFilter",
    MotherID = cms.untracked.int32(511),
    ParticleID = cms.untracked.int32(443),
    NumberDaughters = cms.untracked.int32(2),
    DaughterIDs = cms.untracked.vint32(13, -13),
    MinPt = cms.untracked.vdouble(2.5, 2.5),
    MinEta = cms.untracked.vdouble(-2.5, -2.5),
    MaxEta = cms.untracked.vdouble(2.5, 2.5),
    verbose = cms.untracked.int32(1)
)

kstarfilter = cms.EDFilter(
    "PythiaDauVFilter",
    MotherID = cms.untracked.int32(511),
    ParticleID = cms.untracked.int32(10311),
    NumberDaughters = cms.untracked.int32(2),
    DaughterIDs = cms.untracked.vint32(321, -211),
    MinPt = cms.untracked.vdouble(0.4, 0.4),
    MinEta = cms.untracked.vdouble(-2.5, -2.5),
    MaxEta = cms.untracked.vdouble(2.5, 2.5),
    verbose = cms.untracked.int32(1)
)


ProductionFilterSequence = cms.Sequence(generator*bfilter*jpsifilter*kstarfilter)
