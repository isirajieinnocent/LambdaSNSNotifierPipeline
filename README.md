 <h1>The Architecture</h1

![image](https://github.com/user-attachments/assets/15374a0b-867d-4e70-895b-a2d1d3338fa5)

<h1>Project Overview</h1>
This project showcases my ability to design and implement a serverless data processing pipeline using AWS services. It automates the ingestion, validation, and categorization of billing data uploaded to an Amazon S3 bucket, ensuring error handling and real-time notifications.


<h1>Solution Overview</h1>
AWS Lambda validates CSV files upon upload, checking:

Date formats (YYYY-MM-DD).

Product categories (e.g., Bakery, Meat).

Accepted currencies (USD, CAD, EUR).

Error Handling:

Invalid files are moved to an Error Bucket.

Issues are reported via AWS SNS notifications for immediate resolution.

File Categorization:

Valid files are transferred to a Processed Bucket.

Original files are deleted post-processing.

### Key Technologies
AWS S3: Storage and event triggers.

AWS Lambda: File validation and processing.

AWS SNS: Real-time error notifications.

Python & Boto3: Implementation of business logic.

Impact
Error Mitigation: Real-time SNS alerts improve transparency and reduce downtime.

Scalability: Serverless design adapts to varying data loads.

Efficiency: Automates a manual, error-prone process, freeing up resources.

Key Achievements
Designed a scalable serverless architecture using AWS Lambda and S3.

Implemented real-time error reporting with AWS SNS.

Automated billing data validation and processing, reducing manual effort.

This project highlights my expertise in AWS serverless architecture, Python development, and system integration. Let me know if you’d like more details about the technical implementation or real-world applications!
