import streamlit as st
from PIL import Image as im
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from pandas.plotting import scatter_matrix

# Configuration de la page
st.set_page_config(page_title="Analyse Beans DataSet", layout="wide")

# Menu barre latérale
st.sidebar.title('Projet 2 ')
menu = st.sidebar.selectbox("Navigation", ["Accueil", "Visualisation", "Rapport"])

if menu == "Accueil":
    st.markdown(
        """
        <div style='text-align:center;'>
        <h1>Beans and Pods<h1>
        </div>
        <h2>Introduction</h2>
        <p>Beans & Pods, une entreprise spécialisée dans la vente de grains de café et de gousses, a récemment étendu ses opérations à une plateforme en ligne avec le soutien d'Angeli VC. Ce rapport fournit une analyse détaillée des ventes par canal (magasin et en ligne), par produit et par région, et propose des recommandations stratégiques pour améliorer les ventes et cibler plus efficacement les clients.</p>
        """, unsafe_allow_html=True
    )

elif menu == "Visualisation":
    try:
        fichier = 'BeansDataSet.csv'
        data = pd.read_csv(fichier)
        pd.set_option('display.width', 100)
        pd.set_option('display.float_format', '{:.2f}'.format)

        # Afficher le DataFrame
        st.title("Analyse du Beans DataSet")
        st.subheader("Aperçu des données")
        st.dataframe(data.head())

    except FileNotFoundError:
        st.error("Erreur de lecture : Le fichier 'BeansDataSet.csv' est introuvable.")
        st.stop()

    # Aperçu des données
    st.subheader("Aperçu des données")
    st.write("Dimensions du dataset : ", data.shape)
    st.write("Nombre de lignes : ", data.shape[0])
    st.write("Nombre de colonnes : ", data.shape[1])

    # Vérification des valeurs manquantes
    st.subheader("Valeurs manquantes")
    st.write(data.isnull().sum())
    st.write(f"Nombre total de valeurs manquantes : {data.isnull().sum().sum()}")

    # Comptage par 'Channel'
    st.subheader("Analyse par Channel")
    if 'Channel' in data.columns:
        channel_count = data.groupby('Channel').size()
        st.write("Comptage des Channel :")
        st.bar_chart(channel_count)

    # Total des ventes par produit
    if {'Robusta', 'Arabica', 'Espresso', 'Lungo', 'Latte', 'Cappuccino'}.issubset(data.columns):
        data['Total vente'] = data[['Robusta', 'Arabica', 'Espresso', 'Lungo', 'Latte', 'Cappuccino']].sum(axis=1)
        
        st.subheader("Total des ventes")
        total_vente = data[['Robusta', 'Arabica', 'Espresso', 'Lungo', 'Latte', 'Cappuccino']].sum()
        st.write(total_vente)

        # Ventes par région
        if 'Region' in data.columns:
            region_ventes = data.groupby('Region')['Total vente'].sum()
            st.subheader("Ventes par Région")
            st.bar_chart(region_ventes)

    # Statistiques descriptives
    st.subheader("Statistiques descriptives")
    st.write(data.describe())

    # Histogrammes
    st.subheader("Histogrammes")
    fig, ax = plt.subplots(figsize=(15, 10))
    data.hist(bins=15, ax=ax, layout=(3, 3), grid=True)
    st.pyplot(fig)

    try:
        fichier = 'BeansDataSet.csv'
        data = pd.read_csv(fichier)

        data.fillna(0, inplace=True)

        st.title("Graphiques de densité pour chaque colonne")

        numeric_cols = data.select_dtypes(include=['number']).columns

        if len(numeric_cols) > 0:
            fig, axes = plt.subplots(nrows=3, ncols=3, figsize=(15, 15))
            axes = axes.flatten()

            for i, col in enumerate(numeric_cols):
                if i < len(axes):
                    sns.kdeplot(data[col], ax=axes[i], fill=True)
                    axes[i].set_title(f"Densité de {col}")

            for j in range(i + 1, len(axes)):
                fig.delaxes(axes[j])

            plt.tight_layout()
            st.pyplot(fig)
        else:
            st.warning("Aucune colonne numérique trouvée dans le dataset.")
    except Exception as e:
        st.error(f"Erreur lors de la génération des graphiques de densité : {e}")

    # Matrice de corrélation
    st.subheader("Matrice de corrélation")
    data_num = data.select_dtypes(include='number')
    fig, ax = plt.subplots(figsize=(15, 10))
    corr = data_num.corr()
    sns.heatmap(corr, annot=True, cmap='coolwarm', fmt='.2f', ax=ax)
    st.pyplot(fig)

    # Boîtes à moustaches
    st.subheader("Boîtes à moustaches")
    fig, ax = plt.subplots(figsize=(15, 15))
    data.plot(kind='box', layout=(3, 3), subplots=True, sharex=False, sharey=False, ax=ax)
    st.pyplot(fig)

    # Pairplot avec Seaborn
    if 'Cappuccino' in data.columns:
        st.subheader("Pairplot (Cappuccino)")
        try:
            pairplot_fig = sns.pairplot(data, hue='Cappuccino', diag_kind="kde")
            st.pyplot(pairplot_fig.fig)
        except Exception as e:
            st.error(f"Erreur dans le pairplot (Cappuccino) : {e}")

        st.subheader("Pairplot (Arabica et Espresso)")
        try:
            pairplot_fig_2 = sns.pairplot(data, hue='Cappuccino', vars=['Arabica', 'Espresso'], diag_kind="kde")
            st.pyplot(pairplot_fig_2.fig)
        except Exception as e:
            st.error(f"Erreur dans le pairplot (Arabica et Espresso) : {e}")

else:
    st.markdown(
        """
        <div style='text-align:center;'>
        <h1>Rapport d'Analyse des Ventes pour Beans & Pods<h1>
        </div>
        <div>
        <h3>1. Analyse des Ventes par Canal (Magasin vs En Ligne)</h3>
        <p>Les données montrent une répartition des ventes significative entre les canaux en magasin et en ligne.</p>
        </div>
        """, unsafe_allow_html=True
    )

    data = {
        "Canal": ["En ligne", "Magasin"],
        "Total des Ventes": ["6,619,931", "7,999,569"],
        "Unités Vendues": [142, 298]
    }

    df = pd.DataFrame(data)

    st.table(df)

    st.markdown(
        """
        <div>
        <p>Bien que les ventes totales soient élevées dans les deux canaux, le canal magasin génère un volume de ventes supérieur aux ventes en ligne, avec un plus grand nombre d'unités vendues. Cela suggère que les magasins physiques continuent de jouer un rôle essentiel pour Beans & Pods. Cependant, les ventes en ligne représentent également une part substantielle et méritent une attention pour maximiser leur potentiel.</p>
        </div>
        <br>
        <br>
        <div>
        <h3>2. Analyse des Ventes par Produit</h3>
        <p>Le tableau ci-dessous présente les ventes totales pour chaque type de produit :</p>
        </div>
        """, unsafe_allow_html=True
    )

    data = {
        "Produit": ["Robusta", "Arabica", "Espresso", "Lungo", "Latte", "Cappuccino"],
        "Total des Ventes": ["5,280,131", "2,553,357", "3,498,562", "1,351,650", "1,267,857", "670,943"]
    }

    df = pd.DataFrame(data)

    st.table(df)

    st.markdown(
        """
        <div>
        <p>Les produits Robusta et Espresso sont les plus populaires, représentant la majorité des ventes totales. En revanche, les produits Lungo, Latte, et surtout le Cappuccino ont des ventes relativement plus faibles, indiquant une opportunité de croissance pour ces articles. Il peut être stratégique de renforcer la promotion de ces produits moins populaires pour attirer l’attention des consommateurs et diversifier la demande.</p>
        </div>
        <br>
        <br>
        <div>
        <h3>3. Analyse des Ventes par Région</h3>
        <p>La répartition des ventes par région est la suivante :</p>
        </div>
        """, unsafe_allow_html=True
    )

    data = {
        "Région": ["Centrale", "Nord", "Sud"],
        "Total des Ventes": ["1,555,088", "2,386,813", "10,677,599"]
    }

    df = pd.DataFrame(data)

    st.table(df)

    st.markdown(
        """
        <div>
        <p>La région Sud génère le plus grand volume de ventes, suivie par la région Nord et enfin la région Centrale. Ces résultats peuvent indiquer des différences régionales dans les habitudes d'achat ou une plus grande densité de population dans la région Sud. Il serait intéressant d'adapter la stratégie de marketing en fonction de cette répartition géographique.</p>
        </div>
        <br>
        <br>
        <div>
        <h3>Recommandations</h3>
        <ol>
        <li>Renforcer la Stratégie en Magasin.</li>
        <li>Augmenter la Promotion des Ventes en Ligne.</li>
        <li>Accent sur les Produits Robusta et Espresso.</li>
        <li>Stimuler les Ventes des Produits Lungo, Latte et Cappuccino.</li>
        <li>Cibler la Région Sud et Explorer le Potentiel des Régions Nord et Centrale.</li>
        </ol>
        </div>
        <br>
        <br>
        <div>
        <h3>Conclusion</h3>
        <p>Ce rapport met en évidence les forces de Beans & Pods, avec une analyse approfondie des performances par canal, produit et région. Pour optimiser les ventes, il est recommandé de maintenir un équilibre entre les canaux en ligne et en magasin, de se concentrer sur les produits les plus populaires tout en stimulant les ventes des produits moins performants, et de cibler les régions clés. En suivant ces recommandations, Beans & Pods peut non seulement améliorer ses performances actuelles mais aussi explorer de nouvelles opportunités de croissance.</p>
        </div>
        """, unsafe_allow_html=True
    )