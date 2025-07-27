# MongoDB in Docker (RHEL 9)

This project demonstrates running MongoDB inside Docker with authentication and basic CRUD operations.

## Steps
1. Pull MongoDB 4.4 (for CPUs without AVX):
   ```bash
   docker pull mongo:4.4
   ```
2. Run MongoDB container:
   ```bash
   docker run -d --name mongodb -p 27017:27017      -e MONGO_INITDB_ROOT_USERNAME=admin      -e MONGO_INITDB_ROOT_PASSWORD=admin123      mongo:4.4
   ```
3. Connect to MongoDB:
   ```bash
   docker exec -it mongodb mongo -u admin -p admin123
   ```
4. Run test script:
   ```bash
   docker exec -it mongodb mongo -u admin -p admin123 < /mongo_test_script.js
   ```
