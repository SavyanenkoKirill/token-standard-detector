from django.db import models


class Standard(models.Model):
    class TokenType(models.TextChoices):
        ERC20 = "ERC-20"
        ERC721 = "ERC-721"

    class VerificationStatus(models.TextChoices):
        PENDING = "PENDING"
        PROCESSING = "PROCESSING"
        COMPLETED = "COMPLETED"
        FAILED = "FAILED"

    token_type = models.CharField(
        choices=TokenType.choices,
        default=TokenType.ERC20,
        max_length=20
    )
    contract_address = models.CharField(max_length=100)
    source_code = models.TextField()
    is_correct = models.BooleanField(null=True)
    version = models.CharField(max_length=20, null=True)
    status = models.CharField(
        choices=VerificationStatus.choices,
        default=VerificationStatus.PENDING,
        max_length=20
    )
