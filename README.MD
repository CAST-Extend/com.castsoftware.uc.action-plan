# Action Plan Generation Tool

The script is used to to automate the sorting for the Action Plan violations on the database.   

## Installation

* Download and unpack the latest release of Action Plan Generation Tool.
    * Source Code (zip)
    * com.castsoftware.uc.action-plan
    * Unpack the Source Code zip file (arg)

* Add the rules.xlsx file into your Action Plan Generation Tool folder

  
## Usage
The script is designed to run on the command line using 5 parameters, --application, --rules, --output, --host and --port. Used to identify the application, the excel rules file path and the output excel application path.

    python -m cast_action_plan.main -a <application name> -r <rules excel path> -o <output excel path> -n <database host name> -p <database port number>

## General Configuration
The general configuration section contains three parts, 
* host - Database host name
* port - Database port number 
* application - application name
* rules - the absolute location of the excel rules template
* output - the absolute location of the excel output application 

### Output 

This code allows to identify the important violations of the targeted application. The final data are push in the viewer_action_plan table of the corresponding application.
   
### Sample configuration

{
  "project":"Project Name",
  "template":"The absolute location of the excel rules template",
    
  "Configuration":{
      "Database":{
          "database": "postgres",
          "user": "*****",
          "password": "****",
          "host": "<host name>",
          "port": "####"
		  }
    }
}
