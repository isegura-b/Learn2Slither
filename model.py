import pickle
from pathlib import Path


MODELS_DIR = Path(__file__).resolve().parent / "models"


def save_model(q_table, epsilon_by_length, episodes, alpha, gamma, path=None):
    """Save the current training state and return the model path."""

    MODELS_DIR.mkdir(parents=True, exist_ok=True)

    if path is None:
        model_path = MODELS_DIR / ("model_" + str(episodes) + ".pkl")
    else:
        model_path = Path(path)
        if model_path.is_dir():
            model_path = model_path / ("model_" + str(episodes) + ".pkl")
        model_path.parent.mkdir(parents=True, exist_ok=True)

    model_data = {
        "q_table": q_table,
        "epsilon_by_length": epsilon_by_length,
        "episodes": episodes,
        "alpha": alpha,
        "gamma": gamma
    }

    with model_path.open("wb") as model_file:
        pickle.dump(model_data, model_file, protocol=pickle.HIGHEST_PROTOCOL)

    return model_path


def load_model(path, q_table, epsilon_by_length):
    """Load training state while preserving existing dictionary references."""

    model_path = Path(path)
    with model_path.open("rb") as model_file:
        model_data = pickle.load(model_file)

    required_keys = {
        "q_table",
        "epsilon_by_length",
        "episodes",
        "alpha",
        "gamma"
    }
    missing_keys = required_keys.difference(model_data)
    if missing_keys:
        raise ValueError(
            "Invalid model file. Missing keys: "
            + ", ".join(sorted(missing_keys))
        )

    q_table.clear()
    q_table.update(model_data["q_table"])

    epsilon_by_length.clear()
    epsilon_by_length.update(model_data["epsilon_by_length"])

    return {
        "episodes": model_data["episodes"],
        "alpha": model_data["alpha"],
        "gamma": model_data["gamma"],
        "path": model_path
    }
