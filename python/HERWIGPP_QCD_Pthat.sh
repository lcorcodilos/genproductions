#!/bin/sh

cd $CMSSW_BASE/src/Configuration/GenProduction/python/
[ ! -f "__init__.py" ] && touch "__init__.py"

PREFIX="HERWIGPP_QCD_Pthat"

(
cat << EOF
15	1.4755000e+09
30	1.1174600e+08
80	2.0388300e+06
170	6.7980200e+04
300	4.0603200e+03
470	3.5432800e+02
800	1.3268500e+01
1400	1.8450500e-01
2200	1.4957600e-03
3000	9.3023000e-06
EOF
) | while read MINCUT XS; do
(
cat << EOF
import FWCore.ParameterSet.Config as cms

configurationMetadata = cms.untracked.PSet(
	version = cms.untracked.string('$Revision: 1.2 $'),
	name = cms.untracked.string('$Source: /cvs_server/repositories/CMSSW/CMSSW/Configuration/GenProduction/python/HERWIGPP_QCD_Pthat.sh,v $'),
	annotation = cms.untracked.string('Summer09: Herwig++ generation of QCD events, 10TeV, MRST2001, pthat > __MINCUT__ GeV')
)

from Configuration.GenProduction.HerwigppDefaults_cfi import *

source = cms.Source("EmptySource")
generator = cms.EDFilter("ThePEGGeneratorFilter",
	herwigDefaultsBlock,

	configFiles = cms.vstring(),
	parameterSets = cms.vstring(
		'cm10TeV',
		'pdfMRST2001',
		'Summer09QCDParameters',
		'basicSetup',
		'setParticlesStableForDetector',
	),

	Summer09QCDParameters = cms.vstring(
		'cd /Herwig/MatrixElements/',
		'insert SimpleQCD:MatrixElements[0] MEQCD2to2',

		'cd /',
		'set /Herwig/Cuts/JetKtCut:MinKT __MINCUT__*GeV',
		'set /Herwig/UnderlyingEvent/MPIHandler:Algorithm 1',
	),

	crossSection = cms.untracked.double(__XS__),
	filterEfficiency = cms.untracked.double(1.0),
)

ProductionFilterSequence = cms.Sequence(generator)
EOF
) | sed -e "s/__MINCUT__/$MINCUT/;s/__XS__/$XS/" > ${PREFIX}_${MINCUT}_10TeV_cff.py

	CONDITION="FrontierConditions_GlobalTag,IDEAL_31X::All"
	# GEN config files
	cmsDriver.py Configuration/GenProduction/python/${PREFIX}_${MINCUT}_10TeV_cff.py \
		--customise Configuration/GenProduction/HERWIGPP_custom.py \
		-s GEN:ProductionFilterSequence \
		--mc --eventcontent RAWSIM --datatier GEN \
		--conditions $CONDITION --no_exec -n 1000
	# GEN-HLT config files
	cmsDriver.py Configuration/GenProduction/python/${PREFIX}_${MINCUT}_10TeV_cff.py \
		--customise Configuration/GenProduction/HERWIGPP_custom.py \
		-s GEN:ProductionFilterSequence,SIM,DIGI,L1,DIGI2RAW,HLT:1E31 \
		--mc --eventcontent RAWSIM --datatier GEN-SIM-RAW \
		--conditions $CONDITION --no_exec -n 10
done
