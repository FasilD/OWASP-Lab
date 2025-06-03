### **Scenario 1: Insecure Direct Object Reference (IDOR)**

**URL:** `/message/<id>`

- **What type of access control flaw is this?**  
    IDOR is a _horizontal access control_ flaw. It occurs when the application exposes references (like `message/1`, `message/2`) to internal objects, and does not verify whether the current user is authorized to access them.
    
- **How could a malicious user exploit this?**  
    A logged-in user could change the message ID in the URL (e.g., `/message/2`) and access someone else's private message without permission, even if they are not the owner.
    
- **Suggest one mitigation strategy:**  
    Always validate ownership before displaying data. For example:

```
    if message.user_id != session['user_id']:     return "Access Denied", 403
```
    

---

### **Scenario 2: Function-Level Access Control Bypass**

**URL:** `/admin`

- **What’s missing from the access control check here?**  
    The route does check for `session['role'] == 'admin'`, but if that check were missing or easily bypassed (e.g., via role tampering), it would allow any authenticated user to access the admin panel.
    
- **What risks would exist if an attacker accesses this?**  
    The attacker might gain access to sensitive admin functionalities like user management, data deletion, or configuration changes.
    
- **How would you fix it?**  
    Enforce strict server-side checks like:
   
```
    if 'user_id' not in session or session.get('role') != 'admin':     return "Access Denied", 403
```
    
    And never rely on client-side role indicators.
    

---

### **Scenario 3: Role Tampering**

**URL:** `/edit_profile`

- **How can a user escalate privileges in this form?**  
    By intercepting and modifying the form data (e.g., changing their role from `user` to `admin`), the user might escalate their privileges.
    
- **Is the user input properly validated?**  
    Partially. There’s an attempt to block role changes for non-admins, but if logic is not enforced strictly or bypassable (e.g., API manipulation), it could be vulnerable.
    
- **Suggest a secure fix:**  
    Never trust user input for roles. Instead:
    
    - Don’t allow role updates from the frontend unless it's explicitly an admin action.
    - Always enforce server-side validation:

```
if session['role'] != 'admin':     user.role = current_role  # do not allow change
```
