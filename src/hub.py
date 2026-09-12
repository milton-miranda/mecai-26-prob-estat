"""
Sincronização de dados com o dataset compartilhado do time no Hugging Face Hub.

O dataset é público, então leitura direta com pandas não precisa de token:
    pd.read_parquet(f"hf://datasets/{HF_REPO_ID}/interim/diesel/diesel.parquet")

Upload precisa de um token de escrita (`huggingface_token` no `.env`, não versionado).
"""

from pathlib import Path

from huggingface_hub import HfApi

from src.config import HF_REPO_ID, HF_TOKEN

api = HfApi(token=HF_TOKEN)


def push_file(local_path: Path, path_in_repo: str) -> None:
    api.upload_file(
        path_or_fileobj=str(local_path),
        path_in_repo=path_in_repo,
        repo_id=HF_REPO_ID,
        repo_type="dataset",
    )
    print(f"{local_path} -> hf://datasets/{HF_REPO_ID}/{path_in_repo}")


def push_folder(local_dir: Path, path_in_repo: str) -> None:
    api.upload_folder(
        folder_path=str(local_dir),
        path_in_repo=path_in_repo,
        repo_id=HF_REPO_ID,
        repo_type="dataset",
    )
    print(f"{local_dir}/ -> hf://datasets/{HF_REPO_ID}/{path_in_repo}/")


def pull_folder(path_in_repo: str, local_dir: Path) -> None:
    local_dir.mkdir(parents=True, exist_ok=True)
    api.snapshot_download(
        repo_id=HF_REPO_ID,
        repo_type="dataset",
        allow_patterns=[f"{path_in_repo}/*"],
        local_dir=local_dir.parent,
    )
    print(f"hf://datasets/{HF_REPO_ID}/{path_in_repo}/ -> {local_dir}/")


def push_diesel() -> None:
    from src.config import DATA_INTERIM, DATA_PROCESSED

    push_folder(DATA_INTERIM / "diesel", "interim/diesel")
    push_folder(DATA_PROCESSED / "diesel", "processed/diesel")

def push_producao_feijao() -> None:

    from src.config import DATA_PROCESSED
    push_folder(DATA_PROCESSED / "safra", "processed/safra")
    
    
if __name__ == "__main__":
    # push_diesel()
    push_producao_feijao()