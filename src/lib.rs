use pyo3::prelude::*;
use pyo3::exceptions::PyValueError;

use ::encipher as encipher_lib;


#[pyclass]
struct Encipher {
    inner: encipher_lib::Encipher,
}

#[pymethods]
impl Encipher {

    #[new]
    #[pyo3(signature = (step, key=None, key_env=None))]
    fn new(step: u8, key: Option<u64>, key_env: Option<&str>) -> PyResult<Self> {
        let inner = encipher_lib::Encipher::new(key, key_env, step)
            .map_err(|e| PyValueError::new_err(e.to_string()))?;
        Ok(Encipher { inner })
    }

    fn encrypt(&self, data: &[u8]) -> PyResult<String> {
        let text = std::str::from_utf8(data)
            .map_err(|e| PyValueError::new_err(e.to_string()))?;
        Ok(self.inner.encrypt(text))
    }

    fn decrypt(&self, token: &str) -> PyResult<Vec<u8>> {
        let json_str = self.inner.decrypt(token)
            .map_err(|e| PyValueError::new_err(e.to_string()))?;
        Ok(json_str.into_bytes())
    }
}

// Register class
#[pymodule]
fn enciphers(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_class::<Encipher>()?;
    Ok(())
}
