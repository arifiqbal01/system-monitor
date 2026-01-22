 if r.status_code in range(400, 600):
            logger.warning(f"Server error {r.status_code} for {website.URL}")
            raise RuntimeError(WebsiteFailure(WebsiteFailureTypes.HTTP, f"Server error {r.status_code}"))