import pandas as pd

test_df = pd.read_json("/Users/ilyaperepelitsa/quant/FERC/FERC/test.json", orient = "index")
test_df.to_csv("/Users/ilyaperepelitsa/quant/FERC/test.csv")
