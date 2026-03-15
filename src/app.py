import json
import os
from datetime import datetime


def lambda_handler(event, context):
    """
    Lambda function invoked by API Gateway.
    Processes scheduled requests from EventBridge Scheduler.
    """
    print('=' * 80)
    print('API GATEWAY INVOCATION - Started')
    print('=' * 80)
    
    log_info('Lambda function invoked via API Gateway', {'event': event})
    
    execution_time = datetime.utcnow().isoformat() + 'Z'
    
    try:
        # Parse request body
        body = json.loads(event.get('body', '{}'))
        source = body.get('source', 'unknown')
        timestamp = body.get('timestamp', execution_time)
        
        print(f'\nExecution Time: {execution_time}')
        print(f'Request Source: {source}')
        print(f'Request Timestamp: {timestamp}')
        
        # Simulate processing work
        print('\nProcessing scheduled task...')
        
        # Example: Process data, call external APIs, update databases, etc.
        processing_result = {
            'requestsProcessed': 1,
            'source': source,
            'receivedAt': timestamp,
            'processedAt': execution_time,
            'status': 'success'
        }
        
        print(f'Request processed successfully')
        print(f'Source: {source}')
        print(f'Status: {processing_result["status"]}')
        
        result = {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'application/json'
            },
            'body': json.dumps({
                'success': True,
                'message': 'Request processed successfully',
                'data': processing_result
            })
        }
        
        log_info('Request completed successfully', {'result': processing_result})
        
        print('\n' + '=' * 80)
        print('API GATEWAY INVOCATION - Completed Successfully')
        print('=' * 80 + '\n')
        
        return result
        
    except Exception as error:
        print('\n' + '=' * 80)
        print('API GATEWAY INVOCATION - Failed')
        print(f'Error: {str(error)}')
        print('=' * 80 + '\n')
        
        log_error('Request processing failed', error, {'executionTime': execution_time})
        
        return {
            'statusCode': 500,
            'headers': {
                'Content-Type': 'application/json'
            },
            'body': json.dumps({
                'success': False,
                'message': 'Request processing failed',
                'error': str(error)
            })
        }


def log_info(message, data=None):
    """Log informational message in JSON format"""
    log_entry = {
        'timestamp': datetime.utcnow().isoformat() + 'Z',
        'level': 'INFO',
        'message': message
    }
    if data:
        log_entry.update(data)
    print(json.dumps(log_entry))


def log_error(message, error, data=None):
    """Log error message in JSON format"""
    log_entry = {
        'timestamp': datetime.utcnow().isoformat() + 'Z',
        'level': 'ERROR',
        'message': message,
        'error': str(error),
        'errorType': type(error).__name__
    }
    if data:
        log_entry.update(data)
    print(json.dumps(log_entry))
