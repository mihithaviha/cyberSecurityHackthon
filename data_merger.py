import pandas as pd
import os

# 1. Load your local starting data
df_small = pd.read_csv('spam.csv')

# 2. Safety check for the external UCI dataset
if os.path.exists('spam_uci.csv'):
    df_uci = pd.read_csv('spam_uci.csv', encoding='latin-1')
    # Use index-based selection to avoid name errors
    df_uci = df_uci.iloc[:, [0, 1]] 
    df_uci.columns = ['label', 'message']
else:
    print("Note: spam_uci.csv not found, proceeding with custom data only.")
    df_uci = pd.DataFrame(columns=['label', 'message'])

# 3. Add Modern Phishing Examples
custom_data = {
    'label': ['spam', 'spam', 'spam', 'spam'],
    'message': [
        "Your Microsoft 365 subscription has expired. Click here to renew.",
        "HR: Please review the updated salary structure in this attachment.",
        "NetFlix: Your payment was declined. Update your card to avoid cancellation.",
        "Crypto Wallet Alert: Unusual withdrawal detected. Click to freeze account."
    ]
}
df_custom = pd.DataFrame(custom_data)

# 4. Merge and Clean
final_df = pd.concat([df_small, df_uci, df_custom], ignore_index=True)
final_df.dropna(inplace=True) # Remove empty rows
final_df['label'] = final_df['label'].str.lower() # Standardize labels

# 5. Save
final_df.to_csv('spam.csv', index=False)
print(f"✅ Dataset upgraded! Total messages: {len(final_df)}")