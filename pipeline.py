# llm_firewall/pipeline.py

from llm_firewall.firewall import PromptFirewall, RetrievalFirewall, ResponseFirewall

class FirewallPipeline:
    def __init__(self, policies, audit_logger):
        self.prompt_fw = PromptFirewall(policies, audit_logger)
        self.retrieval_fw = RetrievalFirewall(policies, audit_logger)
        self.response_fw = ResponseFirewall(policies, audit_logger)

    def run(self, prompt, documents, response):
        prompt_result = self.prompt_fw.check(prompt)
        retrieval_result = self.retrieval_fw.check(documents)
        response_result = self.response_fw.check(response)

        return {
            "prompt": prompt_result,
            "retrieval": retrieval_result,
            "response": response_result,
        }
