from django.core.management.base import BaseCommand
from django.db import connection
import time

class Command(BaseCommand):
    help = 'Monitor database performance'
    
    def handle(self, *args, **options):
        start_time = time.time()
        
        # Test database query performance
        with connection.cursor() as cursor:
            cursor.execute("SELECT COUNT(*) FROM auth_user")
            user_count = cursor.fetchone()[0]
        
        duration = time.time() - start_time
        
        self.stdout.write(f'Database query took {duration:.3f} seconds')
        self.stdout.write(f'Total users: {user_count}')
        
        # Check number of queries
        self.stdout.write(f'Total queries executed: {len(connection.queries)}')
