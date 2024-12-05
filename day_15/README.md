# Day 15
## Today I explored the results and limitations of  PII Redaction and Storage

Commencing with an examination of the outcomes from Stage 1, this section highlights the results obtained from redacting Personally Identifiable Information (PII) and storing them in YAML format.


The results achieved in PII redaction were notably satisfactory. By implementing a rule-based coding methodology, the system effectively identified and redacted various forms of PII, including but not limited to:
- **First Names**
- **Last Names**
- **Email Addresses**
- **Sensitive Numerical Data (e.g., Account Numbers)**

### Key Takeaway
This stage demonstrated strong promise, positioning the system as a viable privacy layer or filter for textual data. It underscores the efficacy of the methodology in safeguarding sensitive information.

---

## Some Limitations

While the implementation of PII redaction yielded notable results, it is essential to acknowledge and address certain limitations:

### 1. **False Negatives**
- **Description**: The system may fail to detect certain PII entities due to:
  - Variations in data formats.
  - Emergence of new PII types.
  - Contextual complexities.
- **Impact**: Undetected sensitive information poses risks to the effectiveness of the anonymization process.

### 2. **False Positives**
- **Description**: Erroneous identification of non-sensitive text as PII, often caused by reliance on:
  - Predefined patterns.
  - Recognition algorithms.
- **Impact**: Unnecessary redaction or modification of non-PII data may affect the accuracy and reliability of the anonymization process.

### 3. **Lack of PII Categorization**
- **Description**: The system can identify PII but lacks granularity in classification.
- **Impact**: While sensitive information is flagged, it cannot be differentiated into specific categories (e.g., name, email, or other data types), limiting its insight capabilities.

### 4. **Absence of Contextual Understanding**
- **Description**: The rule-based approach struggles with contextual nuances, such as distinguishing between:
  - A bank account number.
  - A National Insurance number.
- **Impact**: Limited adaptability to diverse forms of sensitive information reduces accuracy.

---

## Addressing the Limitations
Mitigating these limitations requires:
1. **Customization and Fine-Tuning**:
   - Tailoring Presidio's configuration to the specific use case and data characteristics.
2. **Regular Updates**:
   - Monitoring and updating Presidio’s capabilities to match evolving data patterns.
3. **Contextual Enhancement**:
   - Refining the system's methods to improve contextual understanding.
4. **Risk Mitigation**:
   - Reducing the occurrence of false positives and negatives through iterative improvement.

By addressing these areas, the system can ensure a more precise and contextually aware approach to PII detection and anonymisation, enhancing its utility in privacy engineering applications.
