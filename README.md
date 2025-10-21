# 🎓 Training Center Platform

![Flask](https://img.shields.io/badge/Flask-2.3.3-green)
![Python](https://img.shields.io/badge/Python-3.11-blue)
![MySQL](https://img.shields.io/badge/MySQL-Database-orange)
![TailwindCSS](https://img.shields.io/badge/TailwindCSS-3.4.4-cyan)

Une plateforme web éducative offrant des espaces personnalisés pour apprenants, pédagogues et administrateurs avec intégration d'API OpenAI pour l'assistance pédagogique.

## ✨ Fonctionnalités

### 👥 Système d'authentification multi-rôles
- **Apprenants** : Accès aux outils d'apprentissage et cours
- **Pédagogues** : Interface dédiée pour l'enseignement
- **Administrateurs** : Gestion complète des utilisateurs

### 🛠️ Outils intégrés
- **Assistant IA** : Intégration GPT-3.5-turbo pour l'assistance pédagogique
- **Interface conversationnelle** : Chat en temps réel avec streaming
- **Dashboard personnalisé** : Interface adaptée à chaque type d'utilisateur

### 🔧 Gestion administrative
- Ajout/suppression d'utilisateurs
- Attribution des rôles
- Visualisation de la liste des utilisateurs

## 🚀 Installation

### Prérequis
- Python 3.11+
- MySQL 5.7+
- Node.js (pour TailwindCSS)
- Compte OpenAI (clé API)

### 1. Cloner le projet
```bash
git clone <votre-repo>
cd <nom-du-projet>
```

### 2. Configuration de l'environnement
```bash
# Installer Poetry (gestionnaire de dépendances Python)
pip install poetry

# Installer les dépendances Python
poetry install

# Installer les dépendances Node.js
npm install
```

### 3. Configuration de la base de données
```bash
-- Créer la base de données
CREATE DATABASE training_platform;

-- Créer l\'utilisateur MySQL
CREATE USER 'training_user'@'localhost' IDENTIFIED BY 'password';
GRANT ALL PRIVILEGES ON training_platform.* TO 'training_user'@'localhost';
FLUSH PRIVILEGES;

-- Créer la table users
USE training_platform;
CREATE TABLE users (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(255) UNIQUE NOT NULL,
    usertype ENUM('admin', 'pedagogue', 'apprenant') NOT NULL,
    password VARCHAR(255) NOT NULL
);
```

### 4. Configuration des variables d'environnement
Créez un fichier ```.env``` à la racine du projet :
```bash
OPENAI_API_KEY="votre_clé_api_openai_ici"
```

### 5. Construction des assets CSS
```bash
npx tailwindcss -i ./static/src/css/input.css -o ./static/dist/css/style.css --watch
```

### 6. Lancement de l'application
```bash
python app.py
```
L'application sera accessible à l'adresse : http://127.0.0.1:5000

### 🏗️ Architecture du projet
```text
project/
├── 📁 static/                 # Assets statiques
│   ├── 📁 dist/               # Fichiers compilés
│   │   ├── 📁 css/            # CSS généré
│   │   └── 📁 js/             # JavaScript
│   └── 📁 src/                # Sources TailwindCSS
│       └── 📁 css/
│           └── input.css      # Fichier d'entrée Tailwind
├── 📁 templates/             # Templates Flask/Jinja2
│   ├── index.html             # Page d'accueil
│   ├── login.html            # Connexion
│   ├── dashboard.html        # Tableau de bord
│   ├── tool.html             # Interface chat IA
│   ├── managingAddUsr.html   # Ajout utilisateurs (admin)
│   └── managingDelUsr.html   # Suppression utilisateurs (admin)
├── app.py                    # Application principale Flask
├── pyproject.toml            # Configuration Poetry
├── package.json              # Dépendances Node.js
└── tailwind.config.js        # Configuration TailwindCSS
```

### 🔧 Technologies utilisées
#### Backend
  - Flask 2.3.3 : Framework web Python

  - MySQL : Base de données

  - bcrypt : Hashage des mots de passe

  - WTForms : Validation des formulaires

  - OpenAI API : Intelligence artificielle
#### Frontend
  - TailwindCSS 3.4.4 : Framework CSS utilitaire

  - Bootstrap 4.6.2 : Composants UI

  - Showdown.js : Rendering Markdown

  - Highlight.js : Coloration syntaxique
#### Outils de développement
  - Poetry : Gestion des dépendances Python

  - python-dotenv : Variables d'environnement

### 📊 Routes de l'application

| Route           | Méthode  | Description              | Accès    |
| :---:           | :---:    | :---:                    | :---:    |
| /               | GET      | Page d'accueil           | Public   |
| /login          | GET/POST | Connexion                | Public   |
| /dashboard      | GET      | Tableau de bord          | Connecté |
| /tool           | GET      | Interface chat IA        | Connecté |
| /prompt         | POST     | API chat (streaming)     | Connecté |
| /managingAddUsr | GET/POST | Ajout d'utilisateurs     | Admin    |
| /managingDelUsr | GET/POST | Suppression utilisateurs | Admin    |
| /logout         | GET      | Deconnexion              | Connecté |

### 🔒 Sécurité
  - Hashage bcrypt pour les mots de passe

  - Sessions Flask sécurisées

  - Validation WTForms côté serveur

  - Contrôle d'accès par rôle utilisateur

  - Protection CSRF intégrée

### 🎨 Personnalisation
#### Modification du style
Éditez le fichier ```static/src/css/input.css``` puis reconstruisez :
```bash
npx tailwindcss -i ./static/src/css/input.css -o ./static/dist/css/style.css
```
#### Ajout de modèles OpenAI
Dans ```app.py```, modifiez la ligne :
```bash
model="gpt-3.5-turbo"  # Remplacez par "gpt-4-turbo" si disponible ou la version souhaité, cf. le site OpenAI
```

### 📝 Licence

Ce projet est sous licence MIT. Voir le fichier ```LICENSE``` pour plus de détails.
