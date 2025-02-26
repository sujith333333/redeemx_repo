import React, { useEffect, useState } from 'react'
import { Button, Form, FormControl, InputGroup } from 'react-bootstrap'
import { FaSearch } from 'react-icons/fa'

const SearchBar = ({onSearch}) => {
const [searchItem,setSearchItem]=useState("");
// const handleSearch=()=>{
//     onSearch(searchItem)
// }
useEffect(()=>{
onSearch(searchItem)
},[searchItem])
  return (
    <div>
        <Form className="d-flex">
      <InputGroup>
        <FormControl
          type="search"
          placeholder="Search By name/email"
          className="me-2"
          aria-label="Search"
          onChange={(e)=>setSearchItem(e.target.value)}
        />
        {/* <Button variant="outline-secondary" onClick={handleSearch}>
          <FaSearch />
        </Button> */}
      </InputGroup>
    </Form>
    </div>
  )
}

export default SearchBar