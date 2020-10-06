import * as React from "react";
import {IRootStore} from "../stores/RootStore";

export const AppContext = React.createContext<IRootStore | null>(null);

export const useAppContext = () => {
    const store = React.useContext(AppContext);
    if (!store) {
        throw new Error("Provider Missing!");
    }
    return store;
};
