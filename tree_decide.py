import runpy

sentense = """
Press Respective Number Based on your Requirement:
1. Basis Mode -> Inputs Required:Loan Amount, Interest Rate, Tenure, Loan Start Month -> Press 1
2. Lump Sum Payment Mode -> Press 2
3. Regular Payment Mode -> Press 3
4. Advance/Hybrid Mode -> Press 4

Press Number & Enter your option Here: """
decide = int(input(sentense))
print(decide)
if decide == 1:
    print('Running Vanilla Calculator')
    runpy.run_path("codeBase/vanilla_calculator.py")
elif decide == 2:
    print('Running Lump Sum Calculator')
    runpy.run_path("codeBase/lumpSum_calculator.py")
elif decide == 3:
    print('Running Regular Interval Calculator')
    runpy.run_path("codeBase/regular_interval_calculator.py")
elif decide ==4:
    print('Running Advance Calculator')
    runpy.run_path("codeBase/hybrid_calculator.py")
else:
    print('incorrect Input')

