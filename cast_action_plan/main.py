from cast_action_plan.config import Config
from cast_action_plan.action_plan import ActionPlan
import argparse

if __name__ == '__main__':
    print('\nCAST Action Plan Generation Tool')
    print('Copyright (c) 2022 CAST Software Inc.\n')
    print('If you need assistance, please contact Nevin Kaplan (NKA) from the CAST US PS team\n')

    parser = argparse.ArgumentParser(description='Assessment Action Plan Generation Tool')
    parser.add_argument('-c','--config', required=True, help='Configuration properties file')
    parser.add_argument('-a','--appl_name', required=True, help='Generate action plan for application')
    args = parser.parse_args()

    try:
        db = ActionPlan(Config(args.config))
        db.run(args.appl_name)
    except RuntimeError as re:
        print(re)
        print("Failed to generate Action Plan")        




