
# Install the necessary libs
pip3 install -r requirements.txt

# create and upgrade the database to the latest migration
alembic upgrade head

# run the runner
python3 -m bot