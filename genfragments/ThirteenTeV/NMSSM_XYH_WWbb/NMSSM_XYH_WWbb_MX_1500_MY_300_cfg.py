import FWCore.ParameterSet.Config as cms

from Configuration.Generator.Pythia8CommonSettings_cfi import *
from Configuration.Generator.MCTunes2017.PythiaCP5Settings_cfi import *
from Configuration.Generator.PSweightsPythia.PythiaPSweightsSettings_cfi import *


generator = cms.EDFilter("Pythia8GeneratorFilter",
    maxEventsToPrint = cms.untracked.int32(1),
    pythiaPylistVerbosity = cms.untracked.int32(1),
    filterEfficiency = cms.untracked.double(1.0),
    pythiaHepMCVerbosity = cms.untracked.bool(False),
    comEnergy = cms.double(13000.),
    RandomizedParameters = cms.VPSet(),
)
#cards: https://github.com/cms-sw/genproductions/tree/0ab91e0bb9e011521f6923ace653242f140e782a/bin/MadGraph5_aMCatNLO/cards/production/2017/13TeV/NMSSM_XYH_bbbb/Template

# -------------------------------                                                                                                                                                                                                      
#    Constructing grid                                                                                                                                                                                                                 

XMass = 1500
YMassAndEvents = {
                    300 : 100
                }

for YMass,nEvents in YMassAndEvents.items():

    generator.RandomizedParameters.append(
        cms.PSet(
            ConfigWeight = cms.double(nEvents),
            GridpackPath =  cms.string('/afs/cern.ch/user/l/lcorcodi/public/MC-production/genproductions/bin/MadGraph5_aMCatNLO//NMSSM_XYH_bbbb_MX_1500_MY_%i_slc7_amd64_gcc700_CMSSW_10_6_19_tarball.tar.xz' %(YMass)),
            ConfigDescription = cms.string('YMass_%i' % (YMass)),
            PythiaParameters = cms.PSet(
                pythia8CommonSettingsBlock,
                pythia8CP5SettingsBlock,
                pythia8PSweightsSettingsBlock,
                parameterSets = cms.vstring('pythia8CommonSettings',
                                            'pythia8CP5Settings',
                                            'pythia8PSweightsSettings',
                )
            )
        )
    )

