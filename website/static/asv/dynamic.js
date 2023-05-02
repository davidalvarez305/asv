class DynamicFilter {
  formInputs = {
    originalInputs: {},
    currentInputs: {},
  };
  constructor(inputs) {
    this.formInputs.originalInputs = inputs;

    for (const [key, value] of Object.entries(this.formInputs.originalInputs)) {
      const options = this.createOptionsFactory(value);
      const el = document.getElementById(`${key}`);

      if (el) el.replaceChildren(...options);
    }
  }

  static createOptionsFactory(inputs) {
    let elements = [];
    for (let i = 0; i < inputs.length; i++) {
        const el = document.createElement('option');
        el.value = inputs[i];
        el.innerHTML = inputs[i];
        elements.push(el);
    }
    return elements;
  }
}