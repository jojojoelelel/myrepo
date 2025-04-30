# Deployment Branch

This branch contains the code specifically configured for deployment on AWS infrastructure.

The services in this deployment are containerized using Docker and are hosted across two EC2 instances. Elasticsearch runs as a 2-node cluster (`es01` & `es02`), and the frontend is a React-based Search UI that communicates with the Elasticsearch backend.

## Public Deployment Link

You can access the deployed application here: [http://3.107.8.57:3000](http://3.107.8.57:3000)

For more information on how the deployment was set up, please refer to the architecture diagram in `/deployment-design/`.

## Future Considerations

Note on Deployment Security Configuration
Due to the memory limitations of the free-tier t2.micro EC2 instance type, I chose to deploy the two Elasticsearch nodes (`es01` & `es02`) on separate EC2 instances. As a result, I encountered challenges in generating and distributing the necessary TLS certificates for secure inter-node communication and authentication. To ensure cluster connectivity and avoid blocking progress, I temporarily disabled xpack.security in the deployment setup.

While the assignment did not explicitly require security features to be enabled, I fully acknowledge that deploying without authentication and encryption is not best practice and exposes the service to potential vulnerabilities. That said, I was able to configure certificate-based security in the local version and set up authentication with API keys, and I am confident that with more time, I could figure out the deployment-specific security configuration issues as well.
