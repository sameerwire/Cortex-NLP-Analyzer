# 🛡️ Cortex NLP Phishing Analyzer (Experimental)

A **Cortex analyzer** that uses a fine-tuned BERT model to detect phishing content in emails (`.eml`), Base64-encoded mail, or raw text. Designed to run as a Dockerized analyzer within [TheHive Project's Cortex](https://github.com/TheHive-Project/Cortex), this was an **experimental integration** with the goal of building NLP-based phishing detection into a real-world incident response platform.

> ⚠️ **Note:** This project is currently non-functional within Cortex due to configuration and integration issues. It's being shared for transparency, learning, and potential future improvement.

---

## 🧠 What It Tries to Do

* Uses HuggingFace Transformers and a fine-tuned BERT model (`mrm8488/bert-tiny-finetuned-enron-spam-detection`) to classify email text as phishing or legitimate.
* Parses email data from multiple formats (`file`, `mail`, `text`) and extracts plain-text content from MIME messages.
* Built with Cortex’s `DockerAnalyzer` system in mind, packaged using a lightweight Python Docker image.

---

## ❌ Where It Fails

Despite attempts to align with Cortex’s analyzer framework:

* **Analyzer registration fails** due to `manifest.json` or `baseConfig` issues, possibly related to how Cortex expects internal vs. Docker analyzers.
* `cortexctl` and `DockerAnalyzer` templates did not behave as expected inside Cortex Docker containers.
* Analyzer runs manually but does not function when triggered from Cortex UI/API.

---

## ✅ Still, Here's What Works

### Manual Python Script

You can still run it outside of Cortex using the Python script directly:

```bash
python3 NLP_Phishing_1_0.py --data path/to/email.eml --type file
```

### Docker Image Build

```bash
docker build -t cortex-analyzer-nlp_phishing_1_0:latest analyzer/
```

The image builds successfully, installs all dependencies (Transformers, Torch, CortexUtils), and can be used for standalone execution or debugging.

---

## 🧪 Local Testing (Optional)

```bash
# Convert a .eml email to base64 mail format
python3 test/mailconv.py sample.eml
```

Then use the JSON payload with the analyzer script to test classification outside Cortex.

---

## 📂 Project Structure

```
NLP_Phishing_1_0/
├── analyzer/
│   ├── NLP_Phishing_1_0.py
│   ├── manifest.json
│   ├── config.json
│   ├── Dockerfile
│   └── requirements.txt
├── test/
│   ├── mailconv.py
│   └── sample.eml  # Optional test file
├── README.md
├── LICENSE
└── .gitignore
```

---

## 💡 Why Publish It?

While this project didn’t reach full integration with Cortex, it:

* Demonstrates a working prototype of an NLP phishing detection tool.
* Serves as a foundation for others trying to integrate ML models with TheHive/Cortex.
* Helps document the **gaps in Cortex analyzer documentation** and containerization expectations.

---

## 📃 License

This project is licensed under the **MIT License**. See the [LICENSE](LICENSE) file.
