# Day 9: Addressing Privacy in Software Development

## Challenges of Source Code Leaks

Over the past decade, there have been numerous incidents where source code from major companies was leaked. This is particularly concerning when the leaked code contains sensitive information hidden in variable names or comments. 

Removing such sensitive information often requires obfuscating these names, which makes understanding the code much harder. Since comprehending the code is essential for developers, there’s a frequent trade-off between keeping sensitive information private and maintaining clarity for effective understanding.

## Privacy as an Afterthought in Development

Traditionally, privacy has been addressed late in the software development process, often as an afterthought. By the time privacy concerns are considered, the software is usually already built, which can lead to privacy issues like the "copy problem" and the "bundling problem."

### The Copy Problem
When information is shared, control over it is handed to the recipient. This can lead to misuse, as there are often no technical measures in place to prevent it. The original owner has to weigh the benefits of sharing against the risks.

### The Bundling Problem
It’s often difficult to share one piece of information without sharing additional, related data. This happens either because of technical limitations or because some data is only reliable or useful when shared with other connected pieces.

## Shifting Privacy to the Start of Development

To address these challenges, this project focuses on "shifting privacy left." This means considering privacy from the earliest stages of software development, ensuring privacy teams are involved right from the beginning. 

This proactive approach is becoming more common as privacy laws, such as GDPR (in the UK and EU) and CCPA (in California), require companies to handle privacy issues early. For example, before releasing a product, companies must now address questions about the type of data collected, its purpose, how it’s shared, and where it’s stored.

However, effective communication between engineers and legal teams is often hindered by a lack of shared understanding. To bridge this gap, this project’s first stage focuses on developing solutions to redact Personally Identifiable Information (PII) from text.

## Using Presidio for Privacy Solutions

In the first stage of implementation, Microsoft's Presidio was chosen as a key tool for managing sensitive data. Presidio helps identify and anonymise private information in both text and images. Its flexibility allows for quick deployment and customisation, making it ideal for a wide range of scenarios. 

When combined with third-party PII detection tools like Azure Text Analytics, Presidio can handle cases that third-party services might not fully support.

### Key Features of Presidio
- Predefined or customisable PII detection methods, using techniques like Named Entity Recognition (NER), regular expressions, and rule-based logic.
- Integration with external PII detection models.
- Support for various environments, including Python, PySpark, Docker, and Kubernetes.
- Flexible options for anonymising data, such as redaction, replacement, or encryption.

## Potential Use Cases for Privacy Solutions

The solutions developed aim to enhance privacy in several areas:
1. **Handling PII in Production Systems:** Managing sensitive information in live systems.
2. **Preprocessing Data for ML Models:** Ensuring privacy during machine learning and analytics.
3. **Sanitising Data Pipelines:** Preventing unauthorised access to sensitive data.
4. **Semi-Automated PII Redaction:** Balancing privacy with system usability.
5. **De-identifying Data for Sharing:** Enabling secure data sharing while maintaining privacy.
6. **Pseudonymising Data for Federated Learning:** Using pseudonyms to protect privacy in collaborative learning systems.

### Modules in Presidio
1. **Presidio Analyzer:** Identifies PII within text.
2. **Presidio Anonymizer:** De-identifies PII using methods like redaction, replacement, or encryption.

