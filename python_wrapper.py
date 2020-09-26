# -*- coding: utf-8 -*-
"""
Created on Sat Sep 26 12:26:58 2020

@author: Rucha

This is a python wrapper for dalnrt control-m jobs
Input parameters are 
    product_type_cd : loans, moneymarkets, ..
    region : eur, pac or ams
    mode : start/stop
This wrapper should execute the client app jar by passing required arguments

Usage:
    python python_wrapper.py -prod_cd 'loans' -loc_cd 'eur' -m start
    python python_wrapper.py -prod_cd 'loans' -loc_cd 'eur' -m stop
"""
import argparse
import subprocess
import traceback
import sys
import os
import signal


# Constructing the argument parser
ap = argparse.ArgumentParser()

ap.add_argument("-m", "--mode", required=True,
   help="mode [start/stop]")

ap.add_argument("-prod_cd", "--product_type_cd", required=True,
   help="product_type_cd [loans, moneymarkets ..]")

ap.add_argument("-loc_cd", "--location_cd", required=True,
   help="location_cd - [eur, pac and ams]")
args = vars(ap.parse_args())


def __get_port_number():
    config_port_numbers = {
                        'LOANS' : {'EUR' : 7800 , 'PAC' : 7801, 'AMS' : 7802},
                        'LISTED_DERIVATIVES' : {'EUR' : 7803, 'PAC' : 7804, 'AMS' : 7805},
                        'MONEY_MARKETS' : {'EUR' : 7806, 'PAC' : 7807, 'AMS' : 7808}
                       }
    return config_port_numbers[args['product_type_cd'].upper()][args['location_cd'].upper()]

def __kill_process():
    command = "netstat -ano | findstr {0}".format(__get_port_number)
    c = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr = subprocess.PIPE)
    stdout, stderr = c.communicate()
    pid = int(stdout.decode().strip().split(' ')[-1])
    os.kill(pid, signal.SIGTERM)
    

if args['mode'].upper() == 'START':
    try:
        subprocess.call(['java', '-jar', 'jarname.jar', args['product_type_cd'], args['location_cd']], __get_port_number())
    except:
        #print('Error occured while executing jar');
        traceback.print_exception(*sys.exc_info()) 
elif args['mode'].upper() == 'STOP':
    try:
        __kill_process()
    except:
        #print('Error while killing process')
        traceback.print_exception(*sys.exc_info()) 



