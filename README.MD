# Action Plan Generation Tool

The script is used to automate the sorting for the Action Plan violations on the database.   

## Installation

* Download and unpack the latest release of Action Plan Generation Tool.
    * Source Code (zip)
    * com.castsoftware.uc.action-plan
    * Unpack the Source Code zip file (arg)
  
## Usage
The script is designed to run on the command line using 3 parameters, --application, --rules and --output. Used to identify the application, the excel rules file path and the output excel application path.

    py .\main.py -a <application name> -r <rules excel path> -o <output excel path>

## General Configuration
The general configuration section contains 3 parts,  
* application - application name
* rules - the absolute location of the excel rules template
* output - the absolute location of the excel application output 

### Output 

This code allows to identify the important violations of the targeted application. The final data are pushed in the viewer_action_plan table of the corresponding application.
   
