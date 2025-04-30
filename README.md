# Deployment Branch

This branch contains the code specifically configured for deployment on AWS infrastructure.

The services in this deployment are containerized using Docker and are hosted across two EC2 instances. Elasticsearch runs as a 2-node cluster (`es01`, `es02`), and the frontend is a React-based Search UI that communicates with the Elasticsearch backend.

## Public Deployment Link

You can access the deployed application here: [http://3.107.8.57:3000](http://3.107.8.57:3000)

For more information on how the deployment was set up, please refer to the architecture diagram in `/deployment-design/`.
