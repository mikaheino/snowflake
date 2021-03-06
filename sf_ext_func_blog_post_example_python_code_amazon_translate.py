import json
import logging
import boto3
import os

def lambda_handler(event, context):

    # 200 is the HTTP status code for "ok".
    status_code = 200

    # The return value will contain an array of arrays (one inner array per input row).
    array_of_rows_to_return = [ ]

    try:
        # From the input parameter named "event", get the body, which contains
        # the input rows.
        event_body = event["body"]

        # Convert the input from a JSON string into a JSON object.
        payload = json.loads(event_body)
        # This is basically an array of arrays. The inner array contains the
        # row number, and a value for each parameter passed to the function.
        rows = payload["data"]

        # For each input row in the JSON object...
        for row in rows:
            # Read the input row number (the output row number will be the same).
            row_number = row[0]

            # Read the first input parameter's value. For example, this can be a
            # numeric value or a string, or it can be a compound value such as
            # a JSON structure.
            input_value_1 = row[1]

            # Read the second input parameter's value.
            input_value_2 = row[2]
            
            translate = boto3.client(service_name='translate', region_name='eu-central-1', use_ssl=True)
            
            source_language = "auto"
            target_language = "en"
            
            translated = translate.translate_text(Text=input_value_2, SourceLanguageCode=source_language, TargetLanguageCode=target_language)
            
            # Compose the output based on the input. This simple example
            # merely echoes the input by collecting the values into an array that
            # will be treated as a single VARIANT value.
            output_value = [input_value_1, translated]

            # Put the returned row number and the returned value into an array.
            row_to_return = [row_number, output_value]

            # ... and add that array to the main array.
            array_of_rows_to_return.append(row_to_return)

        json_compatible_string_to_return = json.dumps({"data" : array_of_rows_to_return})

    except Exception as err:
        # 400 implies some type of error.
        status_code = 400
        # Tell caller what this function could not handle.
        json_compatible_string_to_return = event_body

    # Return the return value and HTTP status code.
    return {
        'statusCode': status_code,
        'body': json_compatible_string_to_return
    }