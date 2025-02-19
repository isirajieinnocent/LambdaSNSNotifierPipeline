import csv  # for handling CSV files
import boto3  # for AWS SDK
from datetime import datetime  


#Stage 1: API Call

def get_international_taxes(valid_product_line, billing_bucket, csv_file):
    try:
        # Simulate an API failure by raising an exception
        raise Exception("API failure: International Taxes API is currently unavailable.")
    except Exception as error:
        sns = boto3.client('sns')
        sns_topic_arn = 'arn:aws:sns:us-east-1:050752610040:TaxesAPIConnectionError'
        message = f"Lambda function failed to reach international taxes API for bucket '{billing_bucket}' and file '{csv_file}'. Error: '{error}'."
        
        # Publish error message to SNS
        sns.publish(
            TopicArn=sns_topic_arn,
            Message=message,
            Subject="Lambda API Call Failure"
        )
        print("Published failure to SNS topic.")
        raise error
    
# Stage 2: File Parsing and Validation

def lambda_handler(event, context):
    # Initialize the S3 resource using boto3
    s3 = boto3.client('s3', region_name='us-east-1')

    try:
        # Extract the bucket name and the CSV file name from the 'event' input
        billing_bucket = event['Records'][0]['s3']['bucket']['name']
        csvfile = event['Records'][0]['s3']['object']['key']

        # Define the name of the error and processed buckets
        error_bucket = 'error-rec-bucket'
        processed_bucket = 'project-billing-processed'

        # Download the CSV file from S3
        obj = s3.get_object(Bucket=billing_bucket, Key=csvfile)
        
        # Read and decode the content from bytes to string
        content = obj['Body'].read().decode('utf-8')
        
        # Split the content by lines
        lines = content.splitlines()
        
        # Initialize a flag for error detection
        error_found = False

        # Define valid product lines and valid currencies
        valid_product_line = ['Bakery', 'Meat', 'Dairy']
        valid_currencies = ['USD', 'CAD', 'EUR']
        
    
        
        # Attempt API call for international taxes
        get_international_taxes(valid_product_line, billing_bucket, csvfile)

        # Parse CSV and skip the header line
        csv_reader = csv.reader(lines)
        data = list(csv_reader)[1:]  # Skip header row

        # Check if data has been populated
        if not data:
            print("Error: No data found in CSV file after header.")
            return  # Exit if there is no data

        # Loop through each row in the CSV data
        for row in data:
            # Access and validate each field
            date = row[6]  # Date field
            product_line = row[4]  # Product line field
            currency = row[7]  # Currency field
            bill_amount = float(row[8])  # Bill amount field, parsed as float
            
            # Check if the date is in the correct format (%Y-%m-%d)
            try:
                datetime.strptime(date, '%Y-%m-%d')
            except ValueError:
                # If the format is incorrect, set the error flag to True
                error_found = True
                print(f"Error in record {row[0]}: Incorrect format for date: {date}.")
                break
            
            # Additional validation for product_line and currency
            if product_line not in valid_product_line:
                error_found = True
                print(f"Error in record {row[0]}: Unrecognized Product Line {product_line}.")
                break


        #Stage 3: Error Handling and File Routing

        # Error handling block to copy and delete file if errors are found
        if error_found:
            copy_source = {
                'Bucket': billing_bucket,
                'Key': csvfile
            }

            try:
                # Copy file to error bucket
                s3.copy_object(CopySource=copy_source, Bucket=error_bucket, Key=csvfile)
                print(f"Moved erroneous file to: {error_bucket}")

                # Delete original file from the billing bucket
                s3.delete_object(Bucket=billing_bucket, Key=csvfile)
                print("Deleted original file from bucket.")

            except Exception as e:
                print(f"Error while moving file to error bucket: {str(e)}")
        else:
            # If no errors, move the file to the processed bucket
            copy_source = {
                'Bucket': billing_bucket,
                'Key': csvfile
            }

            try:
                # Copy file to processed bucket
                s3.copy_object(CopySource=copy_source, Bucket=processed_bucket, Key=csvfile)
                print(f"Moved processed file to: {processed_bucket}")

                # Delete original file from the billing bucket
                s3.delete_object(Bucket=billing_bucket, Key=csvfile)
                print("Deleted original file from bucket.")

            except Exception as e:
                print(f"Error while moving file to processed bucket: {str(e)}")

            # Return response if no error found in the CSV files
            return {
                'statusCode': 200,
                'body': 'No error found in the CSV files!'
            }

    except Exception as e:
        print(f"Error in lambda_handler: {str(e)}")
        return {
            'statusCode': 500,
            'body': 'Error processing the CSV file.'
        }
