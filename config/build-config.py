#!/usr/bin/env python3
"""
KrakenD Configuration Builder
Merge multiple endpoint files into single krakend.json
"""

import json
import os

def load_json_file(filepath):
    """Load JSON file and return parsed content"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
            # Remove trailing commas before parsing
            content = content.rstrip().rstrip(',')
            return json.loads(f'[{content}]')  # Wrap in array to parse multiple objects
    except FileNotFoundError:
        print(f"Warning: {filepath} not found, skipping...")
        return []
    except json.JSONDecodeError as e:
        print(f"Error parsing {filepath}: {e}")
        return []

def load_settings():
    """Load host settings"""
    with open('settings/hosts.json', 'r', encoding='utf-8') as f:
        return json.load(f)

def replace_variables(endpoints, hosts):
    """Replace template variables with actual values"""
    json_str = json.dumps(endpoints)
    for key, value in hosts.items():
        json_str = json_str.replace(f'{{{{ .hosts.{key} }}}}', value)
    return json.loads(json_str)

def main():
    """Build final krakend.json from partials"""
    
    # Load settings
    settings = load_settings()
    hosts = settings['hosts']
    
    # Load base config
    with open('krakend.tmpl.json', 'r', encoding='utf-8') as f:
        base_config = json.load(f)
    
    # Load all endpoint partials
    auth_endpoints = load_json_file('partials/endpoints_auth.tmpl')
    generic_endpoints = load_json_file('partials/endpoints_generic.tmpl')
    transaction_endpoints = load_json_file('partials/endpoints_transaction.tmpl')
    
    # Combine all endpoints
    all_endpoints = []
    
    # Add health endpoint from base
    if 'endpoints' in base_config and len(base_config['endpoints']) > 0:
        all_endpoints.append(base_config['endpoints'][0])  # Health endpoint
    
    # Add service endpoints
    all_endpoints.extend(auth_endpoints)
    all_endpoints.extend(generic_endpoints)
    all_endpoints.extend(transaction_endpoints)
    
    # Replace template variables
    all_endpoints = replace_variables(all_endpoints, hosts)
    
    # Create final config
    final_config = {
        "$schema": base_config.get("$schema"),
        "version": base_config.get("version"),
        "name": base_config.get("name"),
        "timeout": base_config.get("timeout"),
        "cache_ttl": base_config.get("cache_ttl"),
        "output_encoding": base_config.get("output_encoding"),
        "port": base_config.get("port"),
        "host": base_config.get("host"),
        "extra_config": base_config.get("extra_config"),
        "endpoints": all_endpoints
    }
    
    # Write to krakend.json
    with open('krakend.json', 'w', encoding='utf-8') as f:
        json.dump(final_config, f, indent=2, ensure_ascii=False)
    
    print(f"✅ Successfully generated krakend.json")
    print(f"   Total endpoints: {len(all_endpoints)}")
    print(f"   - Health: 1")
    print(f"   - Auth Service: {len(auth_endpoints)}")
    print(f"   - Generic Service: {len(generic_endpoints)}")
    print(f"   - Transaction Service: {len(transaction_endpoints)}")

if __name__ == "__main__":
    main()
