# Using AWS for Postgres DB

To update your project to write to a PostgreSQL database hosted on AWS (such as an Amazon RDS instance), make the following changes:

1. Update the connection string in your Spark application (or wherever you are establishing the connection to the PostgreSQL database). The connection string should point to your RDS instance. It usually follows this pattern:

    ```python
    database_url = "postgresql://<username>:<password>@<hostname>:<port>/<dbname>"
    ```

    Replace `<username>`, `<password>`, `<hostname>`, `<port>`, and `<dbname>` with the actual values for your RDS instance.

2. Make sure that your AWS RDS instance is publicly accessible and the security group rules associated with your database allows incoming connections from your application's IP address on the port your DB is listening on (usually 5432 for PostgreSQL).

3. Remove or comment out the `db` service in your `docker-compose.yaml` file since the database is now hosted on AWS, not locally in a Docker container.

    ```yaml
    # db:
    #   image: postgres
    #   restart: always
    #   environment:
    #     POSTGRES_PASSWORD: nrailpassword
    #   volumes:
    #     - ./init.sql:/docker-entrypoint-initdb.d/init.sql
    ```

4. Update your `.env` file to include the new connection details for the AWS RDS instance.

    ```bash
    # PostgreSQL variables
    POSTGRES_USERNAME=your-aws-db-username
    POSTGRES_PASSWORD=your-aws-db-password
    POSTGRES_HOSTNAME=your-aws-db-hostname
    POSTGRES_PORT=your-aws-db-port
    POSTGRES_DBNAME=your-aws-db-name
    ```

5. You'll need to manually create the `darwin` table in your RDS instance, the `init.sql` script was previously used to automatically set up the database schema in the local PostgreSQL container.