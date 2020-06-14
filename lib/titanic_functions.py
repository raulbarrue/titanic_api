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

def clean_df(df, deck = True, title=True, verbose=False):

    df.columns = df.columns.str.lower()

    # Drop "boat", "body", "home.dest" and "ticket". The first two hold information if the passenger survived (boat) or if it didn't and the body was recovered (body).
    ### Why is this not working??
    try:
        df = df.drop(["boat", "body", "home.dest", "ticket"], axis=1)
    except KeyError:
        if verbose:
            print("Any of these features are not in the dataframe: boat, body, home.dest, ticket")


    # Just a few observations, drop them
    df.drop(df[(pd.isnull(df["embarked"]))].index, inplace=True)

    # Replace NULL with median
    df["fare"].fillna(df["fare"].median(), inplace=True)
    df["age"].fillna(df["age"].median(), inplace=True)

    # from: https://triangleinequality.wordpress.com/2013/09/08/basic-feature-engineering-with-the-titanic-data/

    if title:
        # Extract titles
        df["title"] = df["name"].str.extract(r'(Mrs|Mr|Master|Miss|Major|Rev|Dr|Ms|Mlle|Col|Capt|Mme|Countess|Don|Jonkheer)')
        df['title']=df.apply(replace_titles, axis=1)
        df.drop("name", axis=1, inplace=True)

    if deck:
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
    df2 = pd.get_dummies(df, columns=["sex", "embarked", "title", "deck"], prefix="dummy")

    ### CHECK ###
    # Checking if there are any more null values in the dataset. Print the column name if it contains nulls.

    if df2.isnull().values.any():
        for col in df2.columns:    
            if df2[col].count() < df2.shape[0]: #Comparing each column with total number of rows
                n_nan = df2.shape[0] - df2[col].count()
                if verbose:
                    print('Count of NULL in {} ({}): {}'.format(col.upper(),df2[col].dtype, f"{n_nan:,}"))

    else:
        if verbose:
            print("No NULL values in the dataframe")

    return df2

def clean_df_one_observation(df, deck = True, title=True, verbose=False):

    df.columns = df.columns.str.lower()
    

    # dummy categories: "sex", "embarked", "title", "deck"
    sex = ["male", "female"]
    embarked = ["S", "C", "Q"]
    title = ["Mr", "Mrs", "Miss", "Master"]
    deck = ["A", "B", "C", "D", "E", "F", "G", "T", "Unknown"]
    
    # X columns
    columns = ['pclass', 'name', 'sex', 'age', 'sibsp', 'parch', 'fare', 'cabin', 'embarked']
    df = pd.DataFrame(df, columns = columns)

    df["sex"] = df["sex"].astype(pd.CategoricalDtype(sex))
    df["embarked"] = df["embarked"].astype(pd.CategoricalDtype(embarked))

    # from: https://triangleinequality.wordpress.com/2013/09/08/basic-feature-engineering-with-the-titanic-data/

    if title:
        # Extract titles
        df["title"] = df["name"].str.extract(r'(Mrs|Mr|Master|Miss|Major|Rev|Dr|Ms|Mlle|Col|Capt|Mme|Countess|Don|Jonkheer)')
        df['title']=df.apply(replace_titles, axis=1)
        df["title"] = df["title"].astype(pd.CategoricalDtype(title))

        df.drop("name", axis=1, inplace=True)

    if deck:
        # Extracting Deck
        df['deck'] = df["cabin"].str[0].fillna("Unknown")
        df["deck"] = df["deck"].astype(pd.CategoricalDtype(deck))

        df.drop("cabin", axis=1, inplace=True)

    # Creating new family_size column
    df['family_size'] = df['sibsp']+df['parch'] + 1 #counting the passenger itself
    df['fare_per_person'] = df['fare']/df['family_size']
    df['alone'] = df['family_size'].apply(lambda x: 1 if x==1 else 0)

    # Because why not
    df['age*class'] = df['age']*df['pclass']


    # Create final dataframe with dummies
    df2 = pd.get_dummies(df, columns=["sex", "embarked", "title", "deck"], prefix="dummy")

    return df2


# def process_single_input(input_data, model=False):
    
#     # dummy categories: "sex", "embarked", "title", "deck"
#     sex = ["male", "female"]
#     embarked = ["S", "C", "Q"]
#     title = ["Mr", "Mrs", "Miss", "Master"]
#     deck = ["A", "B", "C", "D", "E", "F", "G", "T", "Unknown"]
    
#     # X columns
#     columns = ['pclass', 'name', 'sex', 'age', 'sibsp', 'parch', 'fare', 'cabin', 'embarked']
    
#     # Creating X input dataframe
#     X = pd.DataFrame(input_data, columns = columns)
    
#     ### Data Processing
#     # Extract titles
#     #X["title"] = X["name"].str.extract(r'(Mrs|Mr|Master|Miss|Major|Rev|Dr|Ms|Mlle|Col|Capt|Mme|Countess|Don|Jonkheer)')
#     #X["title"]=X.apply(replace_titles, axis=1)
#     #X.drop("name", axis=1, inplace=True)

#     # Extracting Deck
#     #X['deck'] = X["cabin"].str[0].fillna("Unknown")
#     #X.drop("cabin", axis=1, inplace=True)
    
#     # Creating categories. Otherwise when input is just 1 observation the get_dummies func won't work
#     X["sex"] = X["sex"].astype(pd.CategoricalDtype(sex))
#     X["embarked"] = X["embarked"].astype(pd.CategoricalDtype(embarked))
#     X["title"] = X["title"].astype(pd.CategoricalDtype(title))
#     X["deck"] = X["deck"].astype(pd.CategoricalDtype(deck))
    
#     # Create all the needed features. 
#     # This func was used to train the model.
#     # It'd be a good idea to create a new one just for this purpose since there's not mean age and stuff like that
#     X = clean_df_one_observation(X, deck = False, title = False)
    
#     # Predict outputs
#     #y_pred = model.predict(X)
#     #y_pred_proba = model.predict_proba(X)
    
#     #return y_pred, y_pred_proba
    
#     return X