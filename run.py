
import subprocess
import time
scripts_path = "/home/furkanbk/SDM/P1/preprocess"
data_path = "/home/furkanbk/SDM/P1/data"

def run_script(script_path):
    subprocess.run(['python', script_path])

def main():
    start_time =  time.time()
    # Run scripts in the desired order
    #run bulk_paper_on_field.py
    path = scripts_path + '/bulk_paper_on_field.py'
    run_script(path)
    print("Papers are downloaded.")

    path = scripts_path + '/paper_details.py'
    run_script(path)
    print("Paper details are extracted.")
    
    path = scripts_path + '/written_by.py'
    run_script(path)
    print("Written_by are extracted.")

    path = scripts_path + '/authors.py'
    run_script(path)
    print("Authors are extracted.")

    path = scripts_path + '/affiliations.py'
    run_script(path)
    print("Affiliations are extracted.")

    path = scripts_path + '/published_in.py'
    run_script(path)
    print("Published_in + Conferences + Journals are extracted.")

    path = scripts_path + '/citations.py'
    run_script(path)
    print("Citations are extracted.")

    path = scripts_path + '/reviews.py'
    run_script(path)
    print("Reviews + Reviewed_by are extracted.")

    print("Completed in: ", time.time()-start_time, " seconds")

if __name__ == "__main__":
    main()





#bulk_paper_on_field.py
#paper_details.py
#written_by.py
#authors.py
#affiliations.py