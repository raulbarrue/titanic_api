# Replacing all titles with mr, mrs, miss, master
import pandas as pd

def replace_titles(x):
    title=x['title']
    if title in ['Don', 'Major', 'Capt', 'Jonkheer', 'Rev', 'Col']:
        return 'Mr'
    elif title in ['Countess', 'Mme']:
        return 'Mrs'
    elif title in ['Mlle', 'Ms']:
        return 'Miss'
    elif title =='Dr':
        if x['sex']=='Male':
            return 'Mr'
        else:
            return 'Mrs'
    else:
        return title

def clean_df(df):

    df.columns = df.columns.str.lower()

    # Drop "boat", "body", "home.dest" and "ticket". The first two hold information if the passenger survived (boat) or if it didn't and the body was recovered (body).
    ### Why is this not working??
    try:
        df = df.drop(["boat", "body", "home.dest", "ticket"], axis=1)
    except KeyError:
        print("Any of these features are not in the dataframe: boat, body, home.dest, ticket")


    # Just a few observations, drop them
    df.drop(df[(pd.isnull(df["embarked"]))].index, inplace=True)

    # Replace NULL with median
    df["fare"].fillna(df["fare"].median(), inplace=True)
    df["age"].fillna(df["age"].median(), inplace=True)

    # from: https://triangleinequality.wordpress.com/2013/09/08/basic-feature-engineering-with-the-titanic-data/

    # Extract titles
    df["title"] = df["name"].str.extract(r'(Mrs|Mr|Master|Miss|Major|Rev|Dr|Ms|Mlle|Col|Capt|Mme|Countess|Don|Jonkheer)')
    df['title']=df.apply(replace_titles, axis=1)
    df.drop("name", axis=1, inplace=True)

    # Extracting Deck
    df['deck'] = df["cabin"].str[0].fillna("Unknown")
    df.drop("cabin", axis=1, inplace=True)

    # Creating new family_size column
    df['family_size'] = df['sibsp']+df['parch'] + 1 #counting the passenger itself
    df['fare_per_person'] = df['fare']/df['family_size']
    df['alone'] = df['family_size'].apply(lambda x: 1 if x==1 else 0)

    # Because why not
    df['age*class'] = df['age']*df['pclass']


    # Create final dataframe with dummies
    df2 = pd.get_dummies(df, columns=["sex", "embarked", "title", "deck"], dummy_na=True, prefix="dummy")

    ### CHECK ###
    # Checking if there are any more null values in the dataset. Print the column name if it contains nulls.

    if df2.isnull().values.any():
        for col in df2.columns:    
            if df2[col].count() < df2.shape[0]: #Comparing each column with total number of rows
                n_nan = df2.shape[0] - df2[col].count()
                print('Count of NULL in {} ({}): {}'.format(col.upper(),df2[col].dtype, f"{n_nan:,}"))

    else:
        print("No NULL values in the dataframe")

    return df2