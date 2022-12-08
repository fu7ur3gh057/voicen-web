import React, {useState} from "react";

export function useInput(initialValue: any) {
    const [value, setValue] = useState(initialValue);

    const handleChange = (event: React.ChangeEvent<HTMLInputElement>) => {
        setValue(event.target.value);
        console.log(event.target.value)
    };

    return {
        value,
        onChange: handleChange
    };
}
