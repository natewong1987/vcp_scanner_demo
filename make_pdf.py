

if __name__ == "__main__":
    # this script is support to run external (outside of streamlit to generate the final powerpoint and export into pdf
    # reason is because it needs win32api and cannot work within streamlit
    import datetime
    import os

    from pdf_report_generator.powerpoint_algo import build_pdf_report_from_dir
    #dir = r"C:\Users\tclyu\PycharmProjects\streamlit_deploy_example\report_data_export_2022-04-27"
    dir = r"C:\Users\tclyu\PycharmProjects\streamlit_deploy_example\report_data_export_2022-04-28"
    from streamlit_project_settings import REPORT_OUTPUT_DIR
    output_pdf_path = os.path.join(REPORT_OUTPUT_DIR,"vcp_report_"+str(datetime.datetime.today().date())+".pdf")
    build_pdf_report_from_dir(dir, output_pdf_path)

