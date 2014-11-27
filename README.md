# ATTENTION-MUNITES MODELING
=========

Work-in-Progress
----
A collection of scripts and machine learning programs for backfilling Attention Minutes.

bootstrap.py pip install -r requirements.txt and set os.environ prompt local variables


fabfile.py

spin_up_emr()
check_on_emr()
tear_down_emr()

run_etl()

spin_up_mongodb_cluster() :check on mongod snapshot else force etl
tear_down_mongodb_cluster()
deploy_demo_to_s3()