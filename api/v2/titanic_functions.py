
import pandas as pd

# Replacing all titles with mr, mrs, miss, master
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

def clean_df(df, verbose=False):

    if not isinstance(df, pd.DataFrame):
        df = pd.DataFrame(df, columns = ["pclass", "name", "sex", "age", "sibsp", "parch", "fare", "cabin", "embarked"]).astype({"pclass":"int64","age":"float64","sibsp":"int64","parch":"int64","fare":"float64"})
    df.columns = df.columns.str.lower()

    # Drop "boat", "body", "home.dest" and "ticket". The first two hold information if the passenger survived (boat) or if it didn't and the body was recovered (body).
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

    # Extract titles
    df["title"] = df["name"].str.extract(r'(Mrs|Mr|Master|Miss|Major|Rev|Dr|Ms|Mlle|Col|Capt|Mme|Countess|Don|Jonkheer)')
    df['title']=df.apply(replace_titles, axis=1)
    df = df.drop("name", axis=1)

    # Extract Deck
    df['deck'] = df["cabin"].str[0].fillna("Unknown")
    df = df.drop("cabin", axis=1)

    # Create new family_size column
    df['family_size'] = df['sibsp']+df['parch'] + 1 #counting the passenger itself
    df['fare_per_person'] = df['fare']/df['family_size']
    df['alone'] = df['family_size'].apply(lambda x: 1 if x==1 else 0)

    # Because why not
    df['age*class'] = df['age']*df['pclass']

####################################### CATEGORIES #######################################
# Used to create dummies when passing in one single observation

    # dummy categories: "sex", "embarked", "title", "deck"
    sex = ["male", "female"]
    embarked = ["S", "C", "Q"]
    title = ["Mr", "Mrs", "Miss", "Master"]
    deck = ["A", "B", "C", "D", "E", "F", "G", "T", "Unknown"]    

    df["sex"] = df["sex"].astype(pd.CategoricalDtype(sex))
    df["embarked"] = df["embarked"].astype(pd.CategoricalDtype(embarked))
    df["title"] = df["title"].astype(pd.CategoricalDtype(title))
    df["deck"] = df["deck"].astype(pd.CategoricalDtype(deck))
###############################################################################################


    # Create final dataframe with dummies
    df2 = pd.get_dummies(df, columns=["sex", "embarked", "title", "deck"], prefix="dummy")

    return df2
    