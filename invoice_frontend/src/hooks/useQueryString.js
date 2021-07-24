import { useLocation } from "react-router-dom";
import queryString from 'query-string';

const useQueryString = () => {
    const { search } = useLocation();
    // console.log(search)
    const query = queryString.parse(search);

    return query
}

export default useQueryString;