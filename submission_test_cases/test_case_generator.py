from hypothesis import given, settings, seed
from hypothesis import strategies as st
import json
from dataclasses import dataclass
import inspect


@dataclass
class TestCaseGenerator:
    target_func: callable
    num_of_samples: int = 100

    def __post_init__(self):
        self.generated_test_cases: list = []

    def store_test_cases(self, input_data, result_data, property_name):
        self.generated_test_cases.append(
            {"input": input_data, "result": result_data, "property": property_name}
        )

    def extract_func_info(self):
        func_sig = inspect.signature(self.target_func)
        params = list(func_sig.parameters.values())
        for p in params:
            if p.annotation == inspect._empty:
                raise TypeError(f"type is missing for the param {p}")
        params = [p for p in params]
        return_type = func_sig.return_annotation
        if return_type == inspect._empty:
            raise TypeError(
                f"return type is missing for the func {self.target_func.__name__}"
            )
        return params, return_type

    def generate_strategy(self, param_name, param_type):
        if param_type == int:
            return st.integers()
        elif param_type == float:
            return st.floats()
        elif param_type == str:
            return st.text()
        elif param_type == bool:
            return st.booleans()
        else:
            raise ValueError(f"unsupported param type for: {param_name}")

    def create_test_case(self):
        params, return_type = self.extract_func_info()
        params_st = {
            p.name: self.generate_strategy(p.name, p.annotation) for p in params
        }

        @settings(max_examples=self.num_of_samples)
        @given(**params_st)
        def test_func(**kwargs):
            result = self.target_func(**kwargs)
            self.store_test_cases(kwargs, result, self.target_func.__name__)

        test_func()