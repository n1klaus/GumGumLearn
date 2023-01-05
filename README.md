# GUMGUMLEARN
Your personalized learning companion for the english language

### Setting up the Database
##### Install dbdocs
``` bash
# clean cache and update to the latest version
sudo npm cache clean -f
sudo npm update -g npm

# install dbdocs
sudo npm install -g dbdocs
```

##### Install dbml2sql
``` bash
# install dbml to sql cli tool
npm install -g @dbml/cli
```

##### Install postgresql
``` bash
# Add repository keys and gpg keys
sudo sh -c 'echo "deb http://apt.postgresql.org/pub/repos/apt $(lsb_release -cs)-pgdg main" > /etc/apt/sources.list.d/pgdg.list'
wget --quiet -O - https://www.postgresql.org/media/keys/ACCC4CF8.asc | sudo apt-key add -

# update apt list
sudo apt-get update

# install postgresql
sudo apt-get -y install postgresql postgresql-contrib

# Add working environment variables to user profile
echo -c 'export LC_ALL="en_US.UTF-8"' | sudo tee -a ~/.profile
echo -c 'export PGHOST=localhost' | sudo tee -a ~/.profile
```

##### Creating a single dbml file
``` bash
# move to the database directory
cd backend/database

# Concatenate all files into a single file
# validate and build the project
cat users.dbml vault.dbml search.dbml > learn_db_dev.dbml &&\
dbdocs build learn_db_dev.dbml
```

##### Creating a sqldump from dbml file
``` bash
# create a sql dump from the dbml file
dbml2sql learn_db_dev.dbml -o learn_db_dev.sql
```

### Setting up the Backend
##### [Setup the environment variables](./DEV_ENV.sh)
``` bash
# Add working environment variables to user profile
echo "source /vagrant/GumGumLearn/DEV_ENV.sh" | sudo tee -a ~/.profile
```

##### [Setup the database and user](./database/create_db_dev.sh)
``` bash
# sometimes you may need to run this twice if you get an error

# you may also need to make sure '/etc/postgresql/15/main/pg_hba.conf'
# has local connections to trust, like this:
# local        all      postgres     trust
cat backend/database/setup_db_dev.sql | psql postgres postgres
```

##### View the database and tables
``` bash
# Enter password 'learn_dev_pwd'
psql -U learn_dev -d learn_dev_db -W

# To view the databases
\l

# To view all database tables
\dt+

# To exit the psql cli
\q

```

##### Testing class models
``` bash
# create test user and view dictionary attributes
python3 backend/models/test_models.py
```

### Setting up the API

### Setting up the Frontend
``` bash
# install react, create template and dependencies from boilerplate
npx create-react-app my-app
```