class DatabaseClient:
    async def create(self, table, data):
        """Create a new record in the database."""
        raise NotImplementedError("The 'create' method must be implemented.")
    
    async def read(self, table, query):
        """Read a record from the database by its ID."""
        raise NotImplementedError("The 'read' method must be implemented.")
    
    async def update(self, table, query, data):
        """Update an existing record in the database."""
        raise NotImplementedError("The 'update' method must be implemented.")
    
    async def delete(self, table, query):
        """Delete a record from the database by its ID."""
        raise NotImplementedError("The 'delete' method must be implemented.")

