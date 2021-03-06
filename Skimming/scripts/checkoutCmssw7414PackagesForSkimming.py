#!/usr/bin/env python
# -*- coding: utf-8 -*-
#-# Copyright (c) 2014 - All Rights Reserved
#-#   Raphael Friese <Raphael.Friese@cern.ch>
#-#   Stefan Wayand <stefan.wayand@gmail.com>
#-#   Thomas Mueller <tmuller@cern.ch>

# checkout script for cmssw53x for skimming
# todo: implement logger
# todo: make cmsenv/scramv work

import os
import sys
from optparse import OptionParser

#################################################################################################################


def execCommands(commands):
	for command in commands:
		print ""
		print "command: " + command
		exitCode = 1
		nTrials = 0
		while exitCode != 0:
			if nTrials > 1:
				print "Last command could NOT be executed successfully! Stop program!"
				sys.exit(1)

				#logger.info("{CHECKOUT_COMMAND} (trial {N_TRIAL}):").formal(CHECKOUT_COMMAND = command, N_TRIAL = (nTrials+1))

			if command.startswith("cd"):
				os.chdir(os.path.expandvars(command.replace("cd ", "")))
				exitCode = int((os.path.expandvars(command.replace("cd ", "").strip("/")) != os.getcwd().strip("/")))
			else:
				exitCode = os.system(command)

			nTrials += 1

	return

#################################################################################################################


def getSysInformation():
	sysInformation = {
	"github_username": os.popen("git config user.name").readline().replace("\n", ""),
	"email": os.popen("git config user.email").readline().replace("\n", ""),
	"editor": os.popen("git config core.editor").readline().replace("\n", ""),
	"pwd": os.getcwd()
	}
	return sysInformation


#################################################################################################################


def checkoutPackages(args):
	commands = [
		"cd " + os.path.expandvars("$CMSSW_BASE/src/"),
		# do the git cms-addpkg before starting with checking out cvs repositories

		#MVA & No-PU MET Recipe
		#https://twiki.cern.ch/twiki/bin/viewauth/CMS/MVAMet#Instructions_for_7_4_X
		#Jan's multi-MET Producer
		"git cms-addpkg RecoMET/METPUSubtraction",
		"cd " + os.path.expandvars("$CMSSW_BASE/src/RecoMET/METPUSubtraction/plugins"),
		"wget https://raw.githubusercontent.com/CERN-PH-CMG/cmg-cmssw/CMGTools-from-CMSSW_7_4_3/RecoMET/METPUSubtraction/plugins/PFMETProducerMVATauTau.cc",
		"wget https://raw.githubusercontent.com/CERN-PH-CMG/cmg-cmssw/CMGTools-from-CMSSW_7_4_3/RecoMET/METPUSubtraction/plugins/PFMETProducerMVATauTau.h",
		"cd " + os.path.expandvars("$CMSSW_BASE/src/RecoMET/METPUSubtraction/"),
		"git clone https://github.com/rfriese/RecoMET-METPUSubtraction data -b 74X-13TeV-Summer15-July2015 --depth 1",
		"rm -rf $CMSSW_BASE/src/RecoMET/METPUSubtraction/data/.git/",
		"cd " + os.path.expandvars("$CMSSW_BASE/src/"),
		"sed '/mvaOutputCovU1_\ = GetR/c \ \ mvaOutputCovU1_ = std\:\:pow\(GetResponse\(mvaReaderCovU1_, varForCovU1_\)\* mvaOutputU\_ \* var\_\[\"particleFlow\_U\"\]\, 2\)\;' RecoMET/METPUSubtraction/src/PFMETAlgorithmMVA.cc -i",
		"sed '/mvaOutputCovU2_\ = GetR/c \ \ mvaOutputCovU2_ = std\:\:pow\(GetResponse\(mvaReaderCovU2_, varForCovU2_\)\* mvaOutputU\_ \* var\_\[\"particleFlow\_U\"\]\, 2\)\;' RecoMET/METPUSubtraction/src/PFMETAlgorithmMVA.cc -i",

		"git cms-addpkg PhysicsTools/PatUtils",
		"sed '/pat::MET outMET/a \ \ \  outMET\.setSignificanceMatrix\(srcMET\.getSignificanceMatrix\(\)\)\;' PhysicsTools/PatUtils/plugins/CorrectedPATMETProducer.cc -i",
		"cd " + os.path.expandvars("$CMSSW_BASE/src/PhysicsTools/PatUtils/data"),
		"wget https://github.com/cms-met/cmssw/blob/METCorUnc74X/PhysicsTools/PatUtils/data/Summer15_50nsV4_DATA_UncertaintySources_AK4PFchs.txt",
		"cd " + os.path.expandvars("$CMSSW_BASE/src/"),

		#PF MET with NoHF MET
		#https://twiki.cern.ch/twiki/bin/view/CMS/MissingETUncertaintyPrescription
		#"git cms-merge-topic -u cms-met:METCorUnc74X",

		#Electron cutBased Id and MVA Id
		#https://twiki.cern.ch/twiki/bin/view/CMS/CutBasedElectronIdentificationRun2#Recipe_for_regular_users_for_7_4
		#https://twiki.cern.ch/twiki/bin/view/CMS/MultivariateElectronIdentificationRun2#Recipes_for_7412_Spring15_MVA_tr
		"git cms-merge-topic ikrav:egm_id_7.4.12_v1",

		#Check out Kappa
		"git clone https://github.com/KappaAnalysis/Kappa.git",
		#"scram b -j 4"
	]
	execCommands(commands)
	return


#################################################################################################################


def main():
	parser = OptionParser()
	sysInformation = getSysInformation()

	parser.add_option("--github_username", help="your name as in github. Default: " + sysInformation["github_username"], default=sysInformation["github_username"], nargs='?')
	parser.add_option("--mail", help="your email. Default: " + sysInformation["email"], default=sysInformation["email"], nargs='?')
	parser.add_option("--editor", help="your favorite editor (ex. emacs). Default: " + sysInformation["editor"], default=sysInformation["editor"], nargs='?')
	parser.add_option("--cmssw_version", help="the CMSSW Version to checko out. Default: CMSSW_7_2_2", default="CMSSW_7_2_2", nargs='?')

	#args = parser.parse_args()
	(options, args) = parser.parse_args()
	checkoutPackages(args)


#################################################################################################################


if __name__ == "__main__":
	main()
