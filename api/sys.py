from fastapi import APIRouter

router = APIRouter()

# Policies
@router.get("/v1/sys/policies/acl")
async def api_get_policies():
    return {
        "request_id": "c6f5d6a7-0b47-4e3c-812f-25f3fba9cd8f",
        "policies": [
            "default",
            "my-policy"
        ]
    }

@router.get("/v1/sys/policies/acl/{name}")
async def api_get_policy(name: str):
    return {
        "request_id": "d9c8a7b6-5f4e-4c7d-8b92-19d8f7b6d9e1",
        "policy": {
            "name": name,
            "rules": "path \"secret/*\" { capabilities = [\"read\", \"list\"] }"
        }
    }

@router.post("/v1/sys/policies/acl/{name}")
async def api_create_update_policy(name: str):
    return {
        "request_id": "b18bbcd5-42b3-f9f8-b5f5-d3a9f08d369d",
        "lease_id": "",
        "lease_duration": 0,
        "renewable": False,
        "warnings": None,
        "auth": None
    }

@router.delete("/v1/sys/policies/acl/{name}")
async def api_delete_policy(name: str):
    return {
        "request_id": "c85f6d6a-6bd4-b0f8-6757-08aa08ec8980",
        "lease_id": "",
        "lease_duration": 0,
        "renewable": False,
        "warnings": None,
        "auth": None
    }

# Mounting Secret Engines
@router.get("/v1/sys/mounts")
async def api_get_mounts():
    return {
        "request_id": "19a7b8c6-4f7d-9e4b-84f5-d8a9f7b6d9f8",
        "data": {
            "secret/": {
                "type": "kv",
                "options": {"version": "2"},
                "accessor": "kv_123456"
            }
        }
    }

@router.post("/v1/sys/mounts/{path}")
async def api_mount_secret_engine(path: str):
    return {
        "request_id": "a99ef8d4-0c13-43a9-89a7-112b09b70410",
        "lease_id": "",
        "lease_duration": 0,
        "renewable": False,
        "warnings": None,
        "auth": None
    }

@router.delete("/v1/sys/mounts/{path}")
async def api_unmount_secret_engine(path: str):
    return {
        "request_id": "76f8bbae-d54e-492a-9c0f-9a1c4115a981",
        "lease_id": "",
        "lease_duration": 0,
        "renewable": False,
        "warnings": None,
        "auth": None
    }

# Audit
@router.post("/v1/sys/audit/{path}")
async def api_enable_audit(path: str):
    return {
        "request_id": "ef5c3f6d-9f72-44d9-a5e6-131f20876f97",
        "lease_id": "",
        "lease_duration": 0,
        "renewable": False,
        "warnings": None,
        "auth": None
    }

@router.delete("/v1/sys/audit/{path}")
async def api_disable_audit(path: str):
    return {
        "request_id": "a99ef8d4-0c13-43a9-89a7-112b09b70410",
        "lease_id": "",
        "lease_duration": 0,
        "renewable": False,
        "warnings": None,
        "auth": None
    }

@router.get("/v1/sys/audit")
async def api_get_audit_logs():
    return {
        "request_id": "98fd50d9-130d-8937-0a95-bf89e72867b7",
        "data": {
            "audit/": {
                "type": "file",
                "options": {
                    "path": "/var/log/vault_audit.log"
                }
            }
        }
    }

# System Operations
@router.get("/v1/sys/health")
async def api_health_check():
    return {
        "request_id": "fa78c8d4-983b-48d8-a6f3-d8c3a7b5c9f7",
        "initialized": True,
        "sealed": False,
        "standby": False,
        "performance_standby": False,
        "replication_performance_mode": "disabled",
        "replication_dr_mode": "disabled",
        "server_time_utc": int(datetime.utcnow().timestamp()),
        "version": "1.8.1",
        "cluster_name": "vault-cluster",
        "cluster_id": "7e2bbd88-02c6-e2f3-e593-9ed3127f89da"
    }

@router.get("/v1/sys/seal-status")
async def api_seal_status():
    return {
        "request_id": "d8a7f8d4-54c8-4f5e-b4c7-8d6f7a9b5c8f",
        "sealed": False,
        "t": 3,
        "n": 5,
        "progress": 0,
        "version": "1.8.1",
        "cluster_name": "vault-cluster",
        "cluster_id": "7e2bbd88-02c6-e2f3-e593-9ed3127f89da"
    }

@router.post("/v1/sys/seal")
async def api_seal_vault():
    return {
        "request_id": "76b8c3d9-0e1f-4a98-b4c7-f7b8d6f8c9f9",
        "sealed": True
    }

@router.post("/v1/sys/unseal")
async def api_unseal_vault():
    return {
        "request_id": "e1a9b3c7-8d2f-4a5d-8c3f-9d6a9f8c7d8f",
        "sealed": False
    }

@router.get("/v1/sys/capabilities")
async def api_get_capabilities():
    return {
        "request_id": "c9a8d7f5-4f7e-4d9f-b2c8-f8d7a9b5f9e6",
        "capabilities": ["create", "read", "update", "delete"]
    }
